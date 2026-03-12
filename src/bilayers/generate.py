import os
import sys
import importlib.util
from pathlib import Path
from typing import Optional, Union

from bilayers_schema import Citations, DockerImage, ExecFunction, Input, Output, Parameter

from ._blpath import project_path
from .parse import safe_parse_config


def generate_top_level_text(interface_citation: Citations, citations: dict[str, Citations], output_html: bool = True) -> tuple[str, str]:
    import warnings
    from interfaces.utils import generate_top_level_text as _generate_top_level_text

    warnings.warn(
        "bilayers.generate.generate_top_level_text is deprecated. Use interfaces.utils.generate_top_level_text instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _generate_top_level_text(interface_citation, citations, output_html)


def load_and_run_generate(
    path: Path,
    generated_dir: Path,
    inputs: dict[str, Input],
    outputs: dict[str, Output],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
    docker_image: DockerImage,
    cli_sequence: dict[str, dict],
):
    path = Path(path).resolve()
    spec = importlib.util.spec_from_file_location("external_module", path)
    if not spec:
        print("Error: could not load spec", file=sys.stderr)
        return
    module = importlib.util.module_from_spec(spec)
    if not spec.loader:
        print("Error: no loader for spec", file=sys.stderr)
        return
    spec.loader.exec_module(module)

    return module.generate(generated_dir, inputs, outputs, parameters, display_only, exec_function, citations, docker_image, cli_sequence)


def generate_interface(interface_name: str, config_path: Union[str, Path]) -> None:
    """Main function to parse config and generate files for specified interface (e.g. gradio, jupyter, cellprofiler plugin)."""
    print("Parsing config...")

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image, cli_sequence = safe_parse_config(config_path)

    interfaces_dir = project_path() / "interfaces"

    iface_dir = interfaces_dir / interface_name

    if not iface_dir.is_dir():
        print(f"Interface dir with name: {interface_name} not found")
        return

    generated_dir = interfaces_dir / "generated_folders" / algorithm_folder_name
    os.makedirs(generated_dir, exist_ok=True)

    generate_py = iface_dir / "generate.py"
    if generate_py.exists():
        print(f"Running generate for {interface_name}...")

        load_and_run_generate(generate_py, generated_dir, inputs, outputs, parameters, display_only, exec_function, citations, docker_image, cli_sequence)
    else:
        print(f"No generate.py found for interface: {interface_name}")


def generate_all(config_path: Union[str, Path]) -> None:
    """Main function to parse config and generate files for every interface."""
    print("Parsing config...")

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image, cli_sequence = safe_parse_config(config_path)

    interfaces_dir = project_path() / "interfaces"

    generated_dir = interfaces_dir / "generated_folders" / algorithm_folder_name
    os.makedirs(generated_dir, exist_ok=True)

    for iface_dir in interfaces_dir.iterdir():
        if not iface_dir.is_dir() or iface_dir.name == "generated_folders":
            continue

        generate_py = iface_dir / "generate.py"
        if generate_py.exists():
            print(f"Running generate for {os.path.basename(iface_dir)}...")

            load_and_run_generate(generate_py, generated_dir, inputs, outputs, parameters, display_only, exec_function, citations, docker_image, cli_sequence)
        else:
            print(f"No generate.py found for interface: {str(iface_dir)}")
