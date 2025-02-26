import yaml
import sys
from typing import TypedDict, Any

class CitationEntry(TypedDict):
    name: str
    doi: str
    license: str
    description: str

class Citations(TypedDict):
    algorithm: dict[str, CitationEntry]

class HiddenArgs(TypedDict, total=False):
    cli_tag: str
    value: str
    append_value: bool
    cli_order: int

class ExecFunction(TypedDict):
    name: str
    script: str
    module: str
    cli_command: str
    hidden_args: dict[str, HiddenArgs] | None

class InputOutput(TypedDict, total=False):
    name: str
    type: str
    label: str
    subtype: list[str] # w.r.t type == image
    description: str
    cli_tag: str | None
    cli_order: int | None
    default: str
    optional: bool
    format: list[str]
    folder_name: str
    file_count: str
    section_id: str
    mode: str
    depth: bool | None # w.r.t type == image
    timepoints: bool | None # w.r.t type == image
    tiled: bool | None # w.r.t type == image
    pyramidal: bool | None # w.r.t type == image

class Parameter(TypedDict, total=False):
    name: str
    type: str
    label: str
    description: str
    default: Any
    cli_tag: str | None
    cli_order: int | None
    optional: bool
    section_id: str
    mode: str
    options: list[dict[str, str]] | None # w.r.t type == radio, dropdown
    output_dir_set: bool | None # w.r.t type == textbox 
    interactive: bool | None
    append_value: bool | None # w.r.t type == checkbox
    multiselect: bool | None # w.r.t type == dropdown

class Config(TypedDict):
    citations: Citations
    algorithm_folder_name: str
    exec_function: ExecFunction
    inputs: dict[str, InputOutput]
    outputs: dict[str, InputOutput]
    parameters: dict[str, Parameter]
    display_only: dict[str, Parameter] | None

def parse_config(config_path: str | None = None) -> Config:
    """
    Parses a YAML configuration file.

    Args:
        config_path (str | None): Path to the config file. Defaults to None.

    Returns:
        Config: A structured dictionary containing parsed YAML data.
    """
    if config_path is None:
        config_path = '../../../src/algorithms/classical_segmentation/config.yaml'
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Convert lists to dictionaries using "name" as key
    config["inputs"] = {item["name"]: item for item in config.get("inputs", [])} if isinstance(config.get("inputs"), list) else {}
    config["outputs"] = {item["name"]: item for item in config.get("outputs", [])} if isinstance(config.get("outputs"), list) else {}
    config["parameters"] = {item["name"]: item for item in config.get("parameters", [])} if isinstance(config.get("parameters"), list) else {}
    config["display_only"] = {item["name"]: item for item in config.get("display_only", [])} if isinstance(config.get("display_only"), list) else {}

    # Convert citations to a dictionary using "name" as key
    config["citations"]["algorithm"] = {item["name"]: item for item in config["citations"].get("algorithm", [])} if isinstance(config["citations"].get("algorithm"), list) else {}

    # Convert hidden_args to dictionary
    hidden_args = config["exec_function"].get("hidden_args", [])
    if isinstance(hidden_args, list):
        config["exec_function"]["hidden_args"] = {arg["cli_tag"]: arg for arg in hidden_args}
    else:
        config["exec_function"]["hidden_args"] = {}

    return config

def main(config_path: str | None = None) -> tuple[
    dict[str,InputOutput], 
    dict[str,InputOutput], 
    dict[str,Parameter], 
    dict[str,Parameter] | None, 
    ExecFunction, 
    str, 
    Citations
]:
    """
    Loads the configuration and extracts necessary information.

    Args:
        config_path (str | None): Path to the configuration file.

    Returns:
        tuple containing parsed configuration data.
    """
    config_path = sys.argv[1] if len(sys.argv) > 1 else None

    config: Config = parse_config(config_path)

    inputs: dict[str,InputOutput] = config.get('inputs', {})

    outputs: dict[str,InputOutput] = config.get('outputs', {})

    parameters: dict[str,Parameter] = config.get('parameters', {})

    display_only: dict[str,Parameter] | None = config.get('display_only', {})

    exec_function: ExecFunction = config.get('exec_function', {})
    exec_function.setdefault("name", "")
    exec_function.setdefault("script", "")
    exec_function.setdefault("module", "")
    exec_function.setdefault("cli_command", "")
    exec_function.setdefault("hidden_args", {})

    algorithm_folder_name: str = config.get('algorithm_folder_name', "")

    citations: Citations = config.get('citations', {"algorithm": {}})

    return inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations

if __name__ == "__main__":

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations = main()
    print(f"Inputs: {inputs}")
    print(f"Outputs: {outputs}")
    print(f"Parameters: {parameters}")
    print(f"Display Only: {display_only}")
    print(f"Exec Function: {exec_function}")
    print(f"Folder Name: {algorithm_folder_name}")
    print(f"Citations: {citations}")
