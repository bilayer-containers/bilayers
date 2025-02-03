import yaml
import sys
from typing import TypedDict, List, Optional, Dict, Any, Tuple

class CitationEntry(TypedDict):
    name: str
    doi: str
    license: str
    description: str

class Citations(TypedDict):
    algorithm: List[CitationEntry]

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
    hidden_args: Optional[HiddenArgs]

class InputOutput(TypedDict, total=False):
    name: str
    type: str
    label: str
    subtype: List[str] # w.r.t type == image
    description: str
    cli_tag: Optional[str]
    cli_order: Optional[int]
    default: str
    optional: bool
    format: List[str]
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
    cli_tag: Optional[str]
    optional: bool
    section_id: str
    mode: str
    options: List[Dict[str, str]] # w.r.t type == radio, dropdown
    output_dir_set: bool # w.r.t type == textbox 
    folder_name: str # w.r.t type == files
    file_count: str # w.r.t type == files
    interactive: bool
    append_value: bool # w.r.t type == checkbox
    multiselect: bool # w.r.t type == dropdown

class Config(TypedDict):
    citations: Citations
    algorithm_folder_name: str
    exec_function: ExecFunction
    inputs: List[InputOutput]
    outputs: List[InputOutput]
    parameters: List[Parameter]
    display_only: Optional[List[Parameter]]

def parse_config(config_path: Optional[str] = None) -> Config:
    """
    Parses a YAML configuration file.

    Args:
        config_path (Optional[str]): Path to the config file. Defaults to None.

    Returns:
        Config: A structured dictionary containing parsed YAML data.
    """
    if config_path is None:
        config_path = '../../../src/algorithms/classical_segmentation/config.yaml'
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main(config_path: Optional[str] = None) -> Tuple[
    List[InputOutput], 
    List[InputOutput], 
    List[Parameter], 
    Optional[List[Parameter]], 
    ExecFunction, 
    str, 
    Citations
]:
    """
    Loads the configuration and extracts necessary information.

    Args:
        config_path (Optional[str]): Path to the configuration file.

    Returns:
        Tuple containing parsed configuration data.
    """
    config_path = sys.argv[1] if len(sys.argv) > 1 else None

    config: Config = parse_config(config_path)

    inputs: List[InputOutput] = config.get('inputs', [])

    outputs: List[InputOutput] = config.get('outputs', [])

    parameters: List[Parameter] = config.get('parameters', [])

    display_only: Optional[List[Parameter]] = config.get('display_only', [])

    exec_function: ExecFunction = config.get('exec_function', {})

    algorithm_folder_name: str = config.get('algorithm_folder_name', None)

    citations: Citations = config.get('citations', [])

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