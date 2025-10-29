"""Containerized introspection utilities for running discovery in isolated Docker environments."""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from .discovery import FunctionMetadata, load_discovery_results
from .resolver import PackageSource


@dataclass
class ContainerConfig:
    """Configuration for containerized introspection."""

    image_name: str
    tag: str = "latest"
    base_image: str = "python:3.11-slim"
    work_dir: str = "/workspace"


def _generate_standalone_discovery_script() -> str:
    """
    Generate a standalone Python script for discovery that doesn't depend on bilayers.

    This embeds the discovery logic directly so the Docker image doesn't need bilayers installed.
    """
    # Read the discovery.py file
    discovery_file = Path(__file__).parent / "discovery.py"
    discovery_code = discovery_file.read_text()

    # Find where the actual code starts (after module docstring and imports)
    lines = discovery_code.split('\n')
    code_start = 0

    # Skip module docstring
    if lines[0].strip().startswith('"""'):
        # Check if it's a single-line docstring
        if lines[0].strip().endswith('"""') and lines[0].strip() != '"""':
            code_start = 1
        else:
            # Multi-line docstring
            for i in range(1, len(lines)):
                if lines[i].strip().endswith('"""'):
                    code_start = i + 1
                    break

    # Skip blank lines and imports
    for i in range(code_start, len(lines)):
        stripped = lines[i].strip()
        # Look for the first @dataclass at column 0 (not indented)
        if stripped and not lines[i].startswith(' ') and not lines[i].startswith('\t'):
            if stripped.startswith('@dataclass') or stripped.startswith('class ') or stripped.startswith('def '):
                code_start = i
                break

    # Get only the class and function definitions, not the imports
    discovery_functions = '\n'.join(lines[code_start:])

    # Create a standalone script with all necessary imports
    script = '''#!/usr/bin/env python3
"""Standalone discovery script - runs without bilayers dependency"""

import argparse
import importlib
import inspect
import json
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Callable, Optional, get_type_hints

''' + discovery_functions + '''

# Main CLI
def main():
    parser = argparse.ArgumentParser(description="Discover functions in a module")
    parser.add_argument("module", help="Module name to introspect")
    parser.add_argument("--output", "-o", required=True, help="Output JSON file path")
    parser.add_argument("--include-private", action="store_true", help="Include private functions")
    parser.add_argument("--filter", help="Regex pattern to filter function names")

    args = parser.parse_args()

    try:
        # Run discovery
        results = discover_callables(
            args.module,
            include_private=args.include_private,
            filter_pattern=args.filter,
        )

        # Save results
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_discovery_results(results, output_path)

        print(f"Discovered {len(results)} functions from {args.module}")
        print(f"Results saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    return script


def get_base_image(python_version: str = "3.11") -> str:
    """
    Get the base Docker image for a given Python version.

    Args:
        python_version: Python version (e.g., "3.9", "3.10", "3.11", "3.12")

    Returns:
        Full Docker base image name
    """
    return f"python:{python_version}-slim"


def generate_introspection_dockerfile(
    source: PackageSource,
    requirements: Optional[list[str]] = None,
    python_version: str = "3.11",
) -> str:
    """
    Generate a Dockerfile for introspection environment.

    Args:
        source: Package source to install
        requirements: Additional requirements to install
        python_version: Python version to use (e.g., "3.9", "3.11")

    Returns:
        Dockerfile content as string
    """
    base_image = get_base_image(python_version)
    lines = [
        f"FROM {base_image}",
        "",
        "WORKDIR /workspace",
        "",
        "# Copy only the discovery script (no need for full bilayers)",
        "COPY discovery_script.py /workspace/discovery_script.py",
        "",
    ]

    # Add additional requirements
    if requirements:
        lines.append("# Install additional requirements")
        for req in requirements:
            lines.append(f'RUN pip install --no-cache-dir "{req}"')
        lines.append("")

    # Install the target package based on source type
    if source.source_type.value == "pypi":
        package_spec = source.location
        if source.version:
            package_spec += f"=={source.version}"
        lines.append("# Install target package from PyPI")
        lines.append(f'RUN pip install --no-cache-dir "{package_spec}"')

    elif source.source_type.value == "git":
        git_url = source.location
        if source.ref:
            git_url += f"@{source.ref}"
        lines.append("# Install target package from Git")
        lines.append(f'RUN pip install --no-cache-dir "git+{git_url}"')

    elif source.source_type.value == "local":
        lines.append("# Copy and install local package")
        lines.append("COPY package /workspace/package")
        lines.append("RUN pip install --no-cache-dir /workspace/package")

    lines.extend(
        [
            "",
            "# Set entrypoint for introspection",
            "ENTRYPOINT [\"python\", \"/workspace/discovery_script.py\"]",
        ]
    )

    return "\n".join(lines)


def build_introspection_image(
    source: PackageSource,
    image_name: str,
    tag: str = "introspect",
    requirements: Optional[list[str]] = None,
    python_version: str = "3.11",
) -> str:
    """
    Build a Docker image for introspection.

    Args:
        source: Package source to install
        image_name: Name for the Docker image
        tag: Tag for the image
        requirements: Additional Python requirements
        python_version: Python version (e.g., "3.9", "3.11", "3.12")

    Returns:
        Full image name with tag
    """
    import shutil

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Create standalone discovery script (no bilayers dependency)
        discovery_script = _generate_standalone_discovery_script()
        (tmpdir_path / "discovery_script.py").write_text(discovery_script)

        # Generate Dockerfile
        dockerfile_content = generate_introspection_dockerfile(source, requirements, python_version)
        dockerfile_path = tmpdir_path / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)

        # If local source, copy the package
        if source.source_type.value == "local":
            local_path = Path(source.location).expanduser().resolve()
            if not local_path.exists():
                raise RuntimeError(f"Local package path does not exist: {local_path}")

            # Copy local package to build context
            shutil.copytree(local_path, tmpdir_path / "package", symlinks=True)

        # Build the image with streaming output
        full_image_name = f"{image_name}:{tag}"
        try:
            # Stream output instead of capturing it
            subprocess.run(
                ["docker", "build", "-t", full_image_name, "."],
                cwd=tmpdir_path,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to build Docker image") from e

        return full_image_name


def discover_in_container(
    image_name: str,
    module_name: str,
    include_private: bool = False,
    filter_pattern: Optional[str] = None,
    output_path: Optional[Path] = None,
) -> list[FunctionMetadata]:
    """
    Run discovery inside a Docker container.

    Args:
        image_name: Docker image to use
        module_name: Module to introspect
        include_private: Include private functions
        filter_pattern: Regex pattern to filter function names
        output_path: Optional path to save results JSON

    Returns:
        List of discovered FunctionMetadata
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        container_output = tmpdir_path / "output.json"

        # Build command arguments
        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{tmpdir_path}:/output",
            image_name,
            module_name,
            "--output",
            "/output/output.json",
        ]

        if include_private:
            cmd.append("--include-private")

        if filter_pattern:
            cmd.extend(["--filter", filter_pattern])

        # Run container with output streaming
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to run introspection in container") from e

        # Load results
        results = load_discovery_results(container_output)

        # Save to output path if requested
        if output_path:
            import shutil

            shutil.copy(container_output, output_path)

        return results


def generate_algorithm_dockerfile(
    metadata: FunctionMetadata,
    source: PackageSource,
    python_version: str = "3.11",
    additional_requirements: Optional[list[str]] = None,
) -> str:
    """
    Generate a Dockerfile for running the discovered algorithm.

    Args:
        metadata: Function metadata
        source: Package source
        python_version: Python version (e.g., "3.9", "3.11", "3.12")
        additional_requirements: Additional Python packages

    Returns:
        Dockerfile content
    """
    base_image = get_base_image(python_version)
    lines = [
        f"FROM {base_image}",
        "",
        "WORKDIR /bilayers",
        "",
        "# Install system dependencies",
        "RUN apt-get update && apt-get install -y --no-install-recommends \\",
        "    git \\",
        "    && rm -rf /var/lib/apt/lists/*",
        "",
        "# Copy and install bilayers from local source",
        "COPY bilayers /bilayers/bilayers",
        "RUN pip install --no-cache-dir /bilayers/bilayers",
        "",
    ]

    # Install additional requirements
    if additional_requirements:
        lines.append("# Install additional requirements")
        for req in additional_requirements:
            lines.append(f'RUN pip install --no-cache-dir "{req}"')
        lines.append("")

    # Install target package
    if source.source_type.value == "pypi":
        package_spec = source.location
        if source.version:
            package_spec += f"=={source.version}"
        lines.append("# Install algorithm package from PyPI")
        lines.append(f'RUN pip install --no-cache-dir "{package_spec}"')

    elif source.source_type.value == "git":
        git_url = source.location
        if source.ref:
            git_url += f"@{source.ref}"
        lines.append("# Install algorithm package from Git")
        lines.append(f'RUN pip install --no-cache-dir "git+{git_url}"')

    elif source.source_type.value == "local":
        lines.append("# Copy and install local package")
        lines.append("COPY package /bilayers/package")
        lines.append("RUN pip install --no-cache-dir /bilayers/package")

    lines.extend(
        [
            "",
            "# Copy algorithm spec",
            "COPY algorithm.yaml /bilayers/algorithm.yaml",
            "",
            "# Set up work directory",
            "RUN mkdir -p /bilayers/input /bilayers/output",
            "",
            "# Install gradio for serving interface",
            "RUN pip install --no-cache-dir gradio",
            "",
            "# Expose Gradio default port",
            "EXPOSE 7860",
            "",
            "# Default command: generate and run Gradio interface",
            'CMD ["sh", "-c", "bilayers_cli generate /bilayers/algorithm.yaml --interface gradio && python /bilayers/generated_folders/*/app.py"]',
        ]
    )

    return "\n".join(lines)


def build_algorithm_image(
    metadata: FunctionMetadata,
    source: PackageSource,
    spec_content: str,
    image_name: str,
    tag: str = "latest",
    python_version: str = "3.11",
    additional_requirements: Optional[list[str]] = None,
) -> str:
    """
    Build a Docker image for the discovered algorithm.

    Args:
        metadata: Function metadata
        source: Package source
        spec_content: YAML spec content
        image_name: Docker image name
        tag: Image tag
        python_version: Python version (e.g., "3.9", "3.11", "3.12")
        additional_requirements: Additional requirements

    Returns:
        Full image name with tag
    """
    import shutil

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Copy bilayers project to build context
        project_root = Path(__file__).parent.parent.parent.parent
        bilayers_project_path = tmpdir_path / "bilayers"

        # Copy the entire project (includes src/, pyproject.toml, etc.)
        shutil.copytree(project_root, bilayers_project_path, symlinks=True,
                       ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc', '.pixi', 'node_modules'))

        # Generate Dockerfile
        dockerfile_content = generate_algorithm_dockerfile(metadata, source, python_version, additional_requirements)
        (tmpdir_path / "Dockerfile").write_text(dockerfile_content)

        # Write algorithm spec
        (tmpdir_path / "algorithm.yaml").write_text(spec_content)

        # Copy local package if needed
        if source.source_type.value == "local":
            local_path = Path(source.location).expanduser().resolve()
            if not local_path.exists():
                raise RuntimeError(f"Local package path does not exist: {local_path}")

            shutil.copytree(local_path, tmpdir_path / "package", symlinks=True)

        # Build image with streaming output
        full_image_name = f"{image_name}:{tag}"
        try:
            subprocess.run(
                ["docker", "build", "-t", full_image_name, "."],
                cwd=tmpdir_path,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to build algorithm image") from e

        return full_image_name
