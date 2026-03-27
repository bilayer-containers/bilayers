import os
from pathlib import Path
from typing import Union

from bilayers_interface_shared import generate_top_level_text as _generate_top_level_text
from bilayers_schema import Citations, InterfaceInput

from ._blpath import project_path
from .interface_loader import InterfaceLoader
from .parse import safe_parse_config


def generate_top_level_text(interface_citation: Citations, citations: dict[str, Citations], output_html: bool = True) -> tuple[str, str]:
    import warnings

    warnings.warn(
        "bilayers.generate.generate_top_level_text is deprecated. Use bilayers_interface_shared.generate_top_level_text instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _generate_top_level_text(interface_citation, citations, output_html)


def run_generate(
    interface_name: str,
    loader: InterfaceLoader,
    interface_input: InterfaceInput,
):
    module = loader.load_module(interface_name)
    return module.generate(interface_input)


def generate_interface(interface_name: str, config_path: Union[str, Path]) -> None:
    """Main function to parse config and generate files for specified interface (e.g. gradio, jupyter, cellprofiler plugin)."""
    print("Parsing config...")

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image, cli_sequence = safe_parse_config(config_path)

    interfaces_dir = project_path() / "interfaces"
    loader = InterfaceLoader(interfaces_dir)

    generated_dir = interfaces_dir / "generated_folders" / algorithm_folder_name
    os.makedirs(generated_dir, exist_ok=True)

    interface_input: InterfaceInput = {
        "output_dir": generated_dir,
        "inputs": inputs,
        "outputs": outputs,
        "parameters": parameters,
        "display_only": display_only,
        "exec_function": exec_function,
        "citations": citations,
        "docker_image": docker_image,
        "cli_sequence": cli_sequence,
    }

    try:
        print(f"Running generate for {interface_name}...")
        run_generate(interface_name, loader, interface_input)
    except FileNotFoundError:
        print(f"Interface {interface_name} not found")
        return


def generate_all(config_path: Union[str, Path]) -> None:
    """Main function to parse config and generate files for every interface."""
    print("Parsing config...")

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image, cli_sequence = safe_parse_config(config_path)

    interfaces_dir = project_path() / "interfaces"
    loader = InterfaceLoader(interfaces_dir)

    generated_dir = interfaces_dir / "generated_folders" / algorithm_folder_name
    os.makedirs(generated_dir, exist_ok=True)

    interface_input: InterfaceInput = {
        "output_dir": generated_dir,
        "inputs": inputs,
        "outputs": outputs,
        "parameters": parameters,
        "display_only": display_only,
        "exec_function": exec_function,
        "citations": citations,
        "docker_image": docker_image,
        "cli_sequence": cli_sequence,
    }

    for interface_name in loader.list_interfaces():
        print(f"Running generate for {interface_name}...")
        run_generate(interface_name, loader, interface_input)
