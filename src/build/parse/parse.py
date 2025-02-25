import yaml
import sys
from typing import TypedDict, Any

class CitationEntry(TypedDict):
    name: str
    doi: str
    license: str
    description: str

class Citations(TypedDict):
    algorithm: list[CitationEntry]

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
    hidden_args: list[HiddenArgs] | None

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
    depth: bool # w.r.t type == image
    timepoints: bool # w.r.t type == image
    tiled: bool # w.r.t type == image
    pyramidal: bool # w.r.t type == image

class Parameter(TypedDict, total=False):
    name: str
    type: str
    label: str
    description: str
    default: Any
    cli_tag: str | None
    optional: bool
    section_id: str
    mode: str
    options: list[dict[str, str]] # w.r.t type == radio, dropdown
    output_dir_set: bool # w.r.t type == textbox 
    interactive: bool
    append_value: bool # w.r.t type == checkbox
    multiselect: bool # w.r.t type == dropdown

class Config(TypedDict):
    citations: Citations
    algorithm_folder_name: str
    exec_function: ExecFunction
    inputs: list[InputOutput]
    outputs: list[InputOutput]
    parameters: list[Parameter]
    display_only: list[Parameter] | None

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
    return config

def main(config_path: str | None = None) -> tuple[
    list[InputOutput], 
    list[InputOutput], 
    list[Parameter], 
    list[Parameter] | None, 
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

    inputs: list[InputOutput] = config.get('inputs', [])

    outputs: list[InputOutput] = config.get('outputs', [])

    parameters: list[Parameter] = config.get('parameters', [])

    display_only: list[Parameter] | None = config.get('display_only', []) or []

    exec_function: ExecFunction = config.get('exec_function', ExecFunction(name="", script="", module="", cli_command="", hidden_args=[]))

    algorithm_folder_name: str = config.get('algorithm_folder_name', None)

    citations: Citations = config.get('citations', {"algorithm": []})

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
