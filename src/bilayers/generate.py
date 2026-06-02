import os
from pathlib import Path
from typing import Union

from bilayers_schema import InterfaceInput

from .interface_loader import InterfaceLoader, MissingInterfaceDependencyError
from .parse import safe_parse_config


def run_generate(interface_name: str, loader: InterfaceLoader, interface_input: InterfaceInput):
    generate_fn = loader.load_generate(interface_name)
    return generate_fn(interface_input)


def generate_interface(interface_name: str, config_path: Union[str, Path]) -> None:
    """Main function to parse config and generate files for specified interface (e.g. gradio, jupyter, cellprofiler plugin)."""
    print("Parsing config...")

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image, cli_sequence = safe_parse_config(config_path)

    loader = InterfaceLoader()

    generated_dir = Path.cwd() / "dist" / interface_name / algorithm_folder_name
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

    print(f"Running generate for {interface_name}...")
    run_generate(interface_name, loader, interface_input)


def generate_all(config_path: Union[str, Path]) -> None:
    """Main function to parse config and generate files for every interface."""
    print("Parsing config...")

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image, cli_sequence = safe_parse_config(config_path)

    loader = InterfaceLoader()

    for interface_name in loader.list_interfaces():
        try:
            generated_dir = Path.cwd() / "dist" / interface_name / algorithm_folder_name
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

            print(f"Running generate for {interface_name}...")
            run_generate(interface_name, loader, interface_input)
        except MissingInterfaceDependencyError as e:
            print(e)
            continue
        except Exception as e:
            print(f"Error occurred while generating for {interface_name}: {e}")
            continue
