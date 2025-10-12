import nox
import os
import yaml
import requests
import subprocess
from typing import Optional, Tuple
from pathlib import Path
from tempfile import gettempdir
import bilayers

####################
# Helper functions
####################

def get_local_digest(image: str) -> str:
    """Get local docker image digest (content hash)"""
    try:
        out = subprocess.check_output(
            ["docker", "inspect", "--format={{.Id}}", image],
            stderr=subprocess.STDOUT,
        )
        return out.decode().strip()
    except subprocess.CalledProcessError:
        return ""

def get_remote_digest(org: str, name: str, tag: str) -> str:
    """Get remote digest from DockerHub for a specific tag"""
    url = f"https://hub.docker.com/v2/repositories/{org}/{name}/tags/{tag}/"
    resp = requests.get(url)
    if resp.status_code != 200:
        return ""
    data = resp.json()
    images = data.get("images", [])
    if len(images) == 0:
        return ""
    return images[0].get("digest", "")

def decide_interface_tag(algo_name: str, interface: str, bump_type: str = "minor") -> str:
    """
    Decide correct tag for bilayer/{algo_name}:{version}-{interface}.
    Build candidate first, compare digests, then decide bump or reuse.
    """
    # Check DockerHub for tags
    url = f"https://hub.docker.com/v2/repositories/bilayer/{algo_name}/tags/"
    resp = requests.get(url)
    if resp.status_code != 200:
        return f"1.0.0-{interface}"  # no repo exists yet

    tags = [t["name"] for t in resp.json().get("results", []) if t["name"].endswith(f"-{interface}")]
    if not tags:
        return f"1.0.0-{interface}"

    # Get latest version number
    versions = [t.split(f"-{interface}")[0] for t in tags]
    latest = sorted(versions, key=lambda v: list(map(int, v.split("."))))[-1]
    latest_tag = f"{latest}-{interface}"

    # Compare candidate vs remote
    local_digest = get_local_digest(f"bilayer/{algo_name}:build-candidate")
    remote_digest = get_remote_digest("bilayer", algo_name, latest_tag)

    if local_digest and remote_digest and local_digest == remote_digest:
        # identical then reuse latest
        return latest_tag
    else:
        # bump version
        major, minor, patch = map(int, latest.split("."))
        if bump_type == "major":
            return f"{major+1}.0.0-{interface}"
        elif bump_type == "minor":
            return f"{major}.{minor+1}.0-{interface}"
        else:  # patch
            return f"{major}.{minor}.{patch+1}-{interface}"

####################
# Nox sessions
####################


# /absolute/path/to/bilayers/src/bilayers/
PKG_ROOT = Path(bilayers.__path__[0])
# /absolute/path/to/bilayers/
PROJ_ROOT = (PKG_ROOT / "../..").resolve()

def tmp_path(filename, prefix="bilayers", sep="_"):
    assert type(filename) is str
    assert len(filename) > 0
    assert prefix is not None
    assert sep is not None

    tempdir = gettempdir()
    return Path(tempdir) / f"{prefix}{sep}{filename}"

@nox.session
def run_parse(session: nox.Session) -> None:
    """
    Runs the parse.py script with a specified configuration file.

    Args:
        session (nox.Session): The Nox session object.
    """
    session.install("-e", ".")
    session.install("pyyaml")
    session.cd(PKG_ROOT/"build/parse")
    config_path = Path(session.posargs[0]).resolve()
    session.run("python", "parse.py", config_path)
    session.cd(PROJ_ROOT)


@nox.session
def run_generate(session: nox.Session) -> None:
    """
    Runs the generate.py script with a specified configuration file.

    Args:
        session (nox.Session): The Nox session object.
    """
    session.install("-e", ".")
    session.install("pyyaml", "jinja2", "nbformat", "ipython", "ipywidgets")
    session.cd(PKG_ROOT/"build/parse")
    config_path = Path(session.posargs[0]).resolve()
    session.run("python", "generate.py", config_path)
    session.cd(PROJ_ROOT)


@nox.session
def build_algorithm(session: nox.Session) -> None:
    """
    Pull or build the base Algorithm Docker image.
    This is used only as the BASE_IMAGE for interfaces.
    The final published image will always be under bilayer/*.
    
    Args:
        session (nox.Session): The Nox session object
    """

    def _fallback(platform: Optional[str], image_name: str, algorithm: str) -> None:
        """
        Handles fallback if pulling a Docker image fails by attempting to build locally.

        Args:
            session (nox.Session): The Nox session object.
            platform (Optional[str]): The target platform (e.g., "linux/arm64").
            image_name (str): The name of the Docker image.
            algorithm (str): The name of the algorithm.
        """
        algorithm_path = PKG_ROOT / f"algorithms/{algorithm}"
        dockerfile_path = algorithm_path / "Dockerfile"
        platform_opt: str = "--platform" if platform else ""
        platform = platform or ""
        # Proceed to build from Dockerfile if pull fails
        if os.path.exists(dockerfile_path):
            print("Pull failed; attempting to build locally from Dockerfile.")
            session.run("docker", "buildx", "build", platform_opt, platform, "-t", image_name, "-f", dockerfile_path, algorithm_path)
            # Save the locally built Docker image name in a file
            with open(tmp_path("docker_image_name.txt"), "w") as file:
                file.write(image_name)
        else:
            session.error(f"Neither Docker image on DockerHub nor Dockerfile found for {algorithm}")

    if len(session.posargs) > 0:
        algorithm = session.posargs[0]
        print("Algorithm Name in build_algorithm session: ", algorithm)
    else:
        algorithm = "classical_segmentation"

    print("Building Algorithm Nox-File: ", algorithm)
    image_name = f"{algorithm}"
    print("Image Name: ", image_name)
    config_file_path = PKG_ROOT/f"algorithms/{algorithm}/config.yaml"

    # Start by checking the config file for DockerHub image details
    if os.path.exists(config_file_path):
        print(f"Checking config file at {config_file_path}")
        with open(config_file_path, "r") as file:
            config = yaml.safe_load(file)

        org: Optional[str] = config.get("docker_image", {}).get("org")
        name: Optional[str] = config.get("docker_image", {}).get("name")
        tag: Optional[str] = config.get("docker_image", {}).get("tag")
        platform: Optional[str] = config.get("docker_image", {}).get("platform")

        if not org or not name or not tag:
            _fallback(platform, image_name, algorithm)
            return

        docker_image_name: str = f"{org}/{name}:{tag}"
        algorithm_folder_name: str = config.get("algorithm_folder_name", "")

        # Save the platform details in a file
        # TODO: path-cleanup - use tempfile.gettempdir() here and everywhere else
        with open(tmp_path("platform.txt"), "w") as file:
            file.write(platform or "<none>")

        # Save the algorithm folder name in a file
        with open(tmp_path("algorithm_folder_name.txt"), "w") as file:
            file.write(algorithm_folder_name)

        # Attempt to pull the image from DockerHub
        try:
            print(f"Trying to pull the Docker image: {docker_image_name}")
            # Pyright reports an error since `platform` can be None, while `session.run()` expects `str | PathLike[str]`
            # However, we have a fallback function, that takes care of this scenario
            # Since this is a safe and expected, I have suppress the warning
            session.run("docker", "pull", "--platform", platform, docker_image_name) # pyright: ignore
            print(f"Successfully pulled Docker image from DockerHub: {docker_image_name}")
            # Save the Docker image name in a file
            with open(tmp_path("docker_image_name.txt"), "w") as file:
                file.write(docker_image_name)
        except Exception as e:
            print(f"Failed to pull Docker image from DockerHub. Error: {e}")
            _fallback(platform, image_name, algorithm)

    else:
        # If the config file does not exist, report an error
        session.error(f"Config file not found at {config_file_path}")


@nox.session
def build_interface(session: nox.Session) -> None:
    """
    Build the interface Docker image (Gradio/Jupyter).
    Uses candidate built plus digest comparison to decide the final tag.
    Final image is always tagged under bilayer/{algorithm}:{version}-{interface}.
    """
    session.install("requests", "pyyaml")
    if len(session.posargs) < 2:
        session.error("Must provide at least interface and algorithm arguments")

    interface = session.posargs[0]
    algorithm = session.posargs[1]
    bump_type = session.posargs[2] if len(session.posargs) > 2 else "minor"

    # Load platform, base image, algo folder
    with open("/tmp/platform.txt", "r") as f:
        platform = f.read().strip()
    with open("/tmp/docker_image_name.txt", "r") as f:
        base_image = f.read().strip()
    with open("/tmp/algorithm_folder_name.txt", "r") as f:
        algorithm_folder_name = f.read().strip()
    
    if not base_image:
        session.error("BASE_IMAGE is empty or invalid. Did build_algorithm run first?")

    # Build candidate first
    dockerfile_path = PKG_ROOT/f"build/dockerfiles/{interface.capitalize()}.Dockerfile"
    candidate_name = f"bilayer/{algorithm_folder_name}:build-candidate"
    print("Dockerfile Path: ", dockerfile_path)

    session.run(
        "docker", "buildx", "build",
        "--platform", platform,
        "--build-arg", f"BASE_IMAGE={base_image}",
        "--build-arg", f"FOLDER_NAME={algorithm_folder_name}",
        "-t", candidate_name,
        "-f", dockerfile_path,
        "src/bilayers/build",
    )


    # Decide final tag (reuse or bump)
    final_tag = decide_interface_tag(algorithm_folder_name, interface, bump_type)
    final_image_name = f"bilayer/{algorithm_folder_name}:{final_tag}"

    # Retag candidate -> final
    session.run("docker", "tag", candidate_name, final_image_name)

    print(f"Final image built and tagged as: {final_image_name}")
    if interface == "gradio":
        session.run(
            "docker",
            "buildx",
            "build",
            "--platform",
            platform,
            "--build-arg",
            f"BASE_IMAGE={base_image}",
            "--build-arg",
            f"FOLDER_NAME={algorithm_folder_name}",
            "-t",
            final_image_name,
            "-f",
            dockerfile_path,
            "src/bilayers/build",
        )
    elif interface == "jupyter":
        session.run(
            "docker",
            "buildx",
            "build",
            "--platform",
            platform,
            "--build-arg",
            f"BASE_IMAGE={base_image}",
            "--build-arg",
            f"FOLDER_NAME={algorithm_folder_name}",
            "-t",
            final_image_name,
            "-f",
            dockerfile_path,
            PKG_ROOT/"build",
        )


@nox.session
def install_gradio(session: nox.Session) -> None:
    """Install Gradio"""
    session.install("gradio")


# Testing sessions
@nox.session
def test_parse(session: nox.Session) -> None:
    session.install("-e", ".")
    session.install("pyyaml")
    session.cd(PKG_ROOT/"build/parse")
    config_path = session.posargs[0]
    session.run("python", "parse.py", config_path)
    session.cd(PROJ_ROOT)


@nox.session
def test_generate(session: nox.Session) -> None:
    session.install("-e", ".")
    session.install("pyyaml", "jinja2", "nbformat", "ipython", "ipywidgets")
    session.cd(PKG_ROOT/"build/parse")
    config_path = session.posargs[0]
    session.run("python", "generate.py", config_path)
    session.cd(PROJ_ROOT)


lint_locations = "src", "tests", "noxfile.py"


# to check but do nothing:
# nox -rs lint
# to auto-fix:
# nox -rs lint -- --fix
@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff")
    args = session.posargs or lint_locations
    session.run("ruff", "check", *args)


format_locations = lint_locations


@nox.session
def format(session: nox.Session) -> None:
    session.install("ruff")
    args = session.posargs or format_locations
    session.run("ruff", "format", *args)
