import os
import sys
import importlib.util
from pathlib import Path
from typing import Optional, Union

from ._blpath import project_path
from .parse import safe_parse_config
from .parse import Input, Output, Parameter, ExecFunction, Citations, DockerImage


def generate_top_level_text(interface_citation: Citations, citations: dict[str, Citations], output_html: bool = True) -> tuple[str, str]:
    """
    Generates a title and a full description (including tool, citation, and license information)
    based on the given interface type and citations.

    Args:
        interface_citation (str): The citation of the interface (e.g. "Gradio" or "Jupyter").
        citations (dict[str, Citations]): A dictionary of additional citations, where the key is a name of the tool/interface.

    Returns:
        tuple[str, str]: A title string and a full description string.
    """
    # Default citations for Interfaces and Bilayers
    BILAYERS: Citations = {
        "name": "Bilayers",
        "doi": "",
        "license": "BSD 3-Clause",
        "description": "A Container Specification and CI/CD built for whole-community support",
    }
    assert "name" in interface_citation and interface_citation.get("name"), "Must provide a name for interface citation"

    interface_name = interface_citation.get("name")

    newline = "<br>" if output_html else "\n\n"

    app_descriptions_lines = ["**This interface provides the following tool(s):**"]
    citation_text_lines = ["**This project relies on citations! Please cite ALL of the following if you find this application useful in your research:**"]
    license_info_lines = ["**Licenses of the components:**"]
    app_names_lines = []

    # Iterate through the citations dictionary from the config.
    for name, citation in citations.items():
        app_descriptions_lines.append(f"{name}: {citation.get('description', '')}")
        if citation.get("doi"):
            citation_text_lines.append(f"Cite {name} using {citation.get('doi', 'N/A')}")
        license_info_lines.append(f"{name} is provided under the {citation.get('license', 'Unknown')} license")
        app_names_lines.append(name)

    # Add default citations for "Bilayers" and for the given interface.
    for citation in [BILAYERS, interface_citation]:
        if citation.get("doi"):
            citation_text_lines.append(f"Cite {citation.get('name')} using {citation.get('doi', 'N/A')}")
        license_info_lines.append(f"{citation.get('name')} is provided under the {citation.get('license', 'Unknown')} license")

    title = "+".join(app_names_lines) + f" - Brought to you in {interface_name} by Bilayers"
    # Instead of joining with newlines, join with <br> so that the markdown cell shows line breaks.
    full_description = f"{newline}".join(
        [f"{newline}".join(app_descriptions_lines), f"{newline}".join(citation_text_lines), f"{newline}".join(license_info_lines)]
    )

    return title, full_description


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

    return module.generate(generated_dir, inputs, outputs, parameters, display_only, exec_function, citations, docker_image)


def generate_interface(interface_name: str, config_path: Union[str, Path]) -> None:
    """Main function to parse config and generate files for specified interface (e.g. gradio, jupyter, cellprofiler plugin)."""
    print("Parsing config...")

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image = safe_parse_config(config_path)

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

        load_and_run_generate(generate_py, generated_dir, inputs, outputs, parameters, display_only, exec_function, citations, docker_image)
    else:
        print(f"No generate.py found for interface: {interface_name}")


def generate_all(config_path: Union[str, Path]) -> None:
    """Main function to parse config and generate files for every interface."""
    print("Parsing config...")

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image = safe_parse_config(config_path)

    interfaces_dir = project_path() / "interfaces"

    generated_dir = interfaces_dir / "generated_folders" / algorithm_folder_name
    os.makedirs(generated_dir, exist_ok=True)

    for iface_dir in interfaces_dir.iterdir():
        if not iface_dir.is_dir() or iface_dir.name == "generated_folders":
            continue

        generate_py = iface_dir / "generate.py"
        if generate_py.exists():
            print(f"Running generate for {os.path.basename(iface_dir)}...")

            load_and_run_generate(generate_py, generated_dir, inputs, outputs, parameters, display_only, exec_function, citations, docker_image)
        else:
            print(f"No generate.py found for interface: {str(iface_dir)}")
