import nox
import os
import yaml

@nox.session
def run_parse(session):
    session.install('pyyaml')
    session.cd('src/build/parse')
    config_path = session.posargs[0]
    session.run("python", "parse.py", config_path)
    session.cd('../../..')

@nox.session
def run_generate(session):
    session.install('pyyaml','jinja2', 'nbformat', 'ipython', 'ipywidgets')
    session.cd('src/build/parse')
    config_path = session.posargs[0]
    session.run('python', 'generate.py', config_path)
    session.cd('../../..')

@nox.session
def build_algorithm(session):
    """Build the Algorithm docker Image"""

    def _fallback(platform: str | None, image_name: str, algorithm: str) -> None:
        dockerfile_path = f'src/algorithms/{algorithm}/Dockerfile'
        platform_opt = "--platform" if platform else ""
        platform = platform or ""
        # Proceed to build from Dockerfile if pull fails
        if os.path.exists(dockerfile_path):
            print("Pull failed; attempting to build locally from Dockerfile.")
            session.run('docker', 'buildx', 'build', platform_opt, platform, '-t', image_name, '-f', dockerfile_path, f'src/algorithms/{algorithm}')
            # Save the locally built Docker image name in a file
            with open('/tmp/docker_image_name.txt', 'w') as file:
                file.write(image_name)
        else:
            session.error(f'Neither Docker image on DockerHub nor Dockerfile found for {algorithm}')

    if len(session.posargs) > 0:
        algorithm = session.posargs[0]
        print("Algorithm Name in build_algorithm session: ", algorithm)
    else:
        algorithm = 'classical_segmentation'

    print("Building Algorithm Nox-File: ", algorithm)
    image_name = f'{algorithm}'
    print("Image Name: ", image_name)
    config_file_path = f'src/algorithms/{algorithm}/config.yaml'

    # Start by checking the config file for DockerHub image details
    if os.path.exists(config_file_path):
        print(f'Checking config file at {config_file_path}')
        with open(config_file_path, 'r') as file:
            config = yaml.safe_load(file)

        org: str | None = config.get('docker_image', {}).get('org')
        name: str | None = config.get('docker_image', {}).get('name')
        tag: str | None = config.get('docker_image', {}).get('tag')
        platform: str | None = config.get('docker_image', {}).get('platform')

        if not org or not name or not tag:
            _fallback(platform, image_name, algorithm)
            return

        docker_image_name = f'{org}/{name}:{tag}'
        algorithm_folder_name = config.get('algorithm_folder_name', None)

        # Save the platform details in a file
        with open('/tmp/platform.txt', 'w') as file:
            file.write(platform or "<none>")

        # Save the algorithm folder name in a file
        with open('/tmp/algorithm_folder_name.txt', 'w') as file:
            file.write(algorithm_folder_name)

        # Attempt to pull the image from DockerHub
        try:
            print(f'Trying to pull the Docker image: {docker_image_name}')
            session.run('docker', 'pull', "--platform", platform, docker_image_name)
            print(f'Successfully pulled Docker image from DockerHub: {docker_image_name}')
            # Save the Docker image name in a file
            with open('/tmp/docker_image_name.txt', 'w') as file:
                file.write(docker_image_name)
        except Exception as e:
            print(f'Failed to pull Docker image from DockerHub. Error: {e}')
            _fallback(platform, image_name, algorithm)

    else:
        # If the config file does not exist, report an error
        session.error(f'Config file not found at {config_file_path}')

@nox.session
def build_interface(session):
    """Build the Gradio docker Image"""
    if len(session.posargs) != 2:
        session.error("Must provide interface and algorithm arguments")

    interface = session.posargs[0]
    algorithm = session.posargs[1]
    print("Building Interface Nox-File: ", interface)

    image_name = f'{algorithm}_{interface}_image'
    print("Image Name: ", image_name)

    dockerfile_path = f'src/build/dockerfiles/{interface.capitalize()}.Dockerfile'
    print("Dockerfile Path: ", dockerfile_path)

    # Read the platform from the file
    with open('/tmp/platform.txt', 'r') as file:
        platform = file.read().strip()

    # Read the Docker image name from the file
    with open('/tmp/docker_image_name.txt', 'r') as file:
        base_image = file.read().strip()

    with open('/tmp/algorithm_folder_name.txt', 'r') as file:
        algorithm_folder_name = file.read().strip()

    if interface == 'gradio':
        session.run('docker', 'buildx', 'build', '--platform', platform, '-f', 'Gradio.Dockerfile', '--build-arg',  f'BASE_IMAGE={base_image}', '--build-arg',  f'FOLDER_NAME={algorithm_folder_name}', '-t', image_name, '-f', dockerfile_path, 'src/build')
    elif interface == 'jupyter':
        session.run('docker', 'buildx', 'build', '--platform', platform, '-f', 'Jupyter.Dockerfile', '--build-arg',  f'BASE_IMAGE={base_image}', '--build-arg',  f'FOLDER_NAME={algorithm_folder_name}', '-t', image_name, '-f', dockerfile_path, 'src/build')

@nox.session
def install_gradio(session):
    """Install Gradio"""
    session.install('gradio')

# Testing sessions
@nox.session
def test_parse(session):
    session.install('pyyaml')
    session.cd('src/build/parse')
    config_path = session.posargs[0]
    session.run("python", "parse.py", config_path)
    session.cd('../../..')

@nox.session
def test_generate(session):
    session.install('pyyaml','jinja2', 'nbformat', 'ipython', 'ipywidgets')
    session.cd('src/build/parse')
    config_path = session.posargs[0]
    session.run('python', 'generate.py', config_path)
    session.cd('../../..')
