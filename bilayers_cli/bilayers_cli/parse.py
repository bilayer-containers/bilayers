import yaml
import sys
import pprint
from typing import TypedDict, Any, cast

# Define structured data types for validation and usage
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
    append_value: bool | None
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
    subtype: list[str]  # for 'image' type
    description: str
    cli_tag: str | None # cli_tag would be optional for outputs section
    cli_order: int | None
    default: str
    optional: bool
    format: list[str]
    folder_name: str
    file_count: str
    section_id: str
    mode: str
    depth: bool | None  # for 'image' type
    timepoints: bool | None  # for 'image' type
    tiled: bool | None  # for 'image' type
    pyramidal: bool | None  # for 'image' type

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
    options: list[dict[str, str]] | None  # for 'radio' and 'dropdown'
    output_dir_set: bool | None  # for 'textbox'
    interactive: bool | None
    append_value: bool | None  # for 'checkbox'
    multiselect: bool | None  # for 'dropdown'

class Config(TypedDict):
    citations: Citations
    algorithm_folder_name: str
    exec_function: ExecFunction
    inputs: dict[str, InputOutput]
    outputs: dict[str, InputOutput]
    parameters: dict[str, Parameter]
    display_only: dict[str, Parameter] | None

def parse_config(config_source: str | None) -> Config:
    """
    Parses a YAML configuration file or an existing dictionary.

    Args:
        config_source (str | dict[str, Any] | None): Path to the YAML file or an already loaded dictionary.

    Returns:
        dict[str, Any]: A structured dictionary containing parsed YAML data.
    """

    if isinstance(config_source, dict):
        config = config_source  # Directly use the dictionary if provided
    else:
        # Default config path if not provided
        config_path = config_source or '../src/algorithms/classical_segmentation/config.yaml'

        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML config file not found: {config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file {config_path}: {e}")

    # Helper function to convert lists to dictionaries using 'name' as key
    def convert_list_to_dict(section_name: str) -> dict[str, Any]:
        section = config.get(section_name, [])
        return {item["name"]: item for item in section} if isinstance(section, list) else {}

    # Convert relevant sections
    config["inputs"] = convert_list_to_dict("inputs")
    config["outputs"] = convert_list_to_dict("outputs")
    config["parameters"] = convert_list_to_dict("parameters")
    config["display_only"] = convert_list_to_dict("display_only")

    # Since "citations" and "algorithm" will always be present in a valid spec file
    # (validated before reaching this point), we don't need to check for None.
    # Pyright might falsely assume they could be missing, so we ignore the warning
    if "citations" in config and "algorithm" in config["citations"]: # pyright: ignore
        config["citations"]["algorithm"] = convert_list_to_dict("citations") # pyright: ignore

    # Ignoring Pyright's warning because "hidden_args" will always be present in a valid spec file
    # The spec ensures that "hidden_args" is either a list or missing (not None)
    # We use .get("hidden_args", []) to ensure it defaults to an empty list, preventing None-related issues
    hidden_args = config.get("exec_function", {}).get("hidden_args", []) # pyright: ignore
    # If "hidden_args" is a list, we convert it to a dictionary using "cli_tag" as the key
    # Otherwise, we set it to an empty dictionary to maintain consistency
    config.setdefault("exec_function", {})["hidden_args"] = {arg["cli_tag"]: arg for arg in hidden_args} if isinstance(hidden_args, list) else {}

    return cast(Config, config)

def main(config_source: str | None = None) -> dict[str, Any]:
    """
    Loads configuration from a YAML file path or directly from a dictionary.

    Args:
        config_source (str | None): YAML file path or a dictionary.

    Returns:
        dict[str, Any]: A structured dictionary containing parsed YAML data.
    """
    config: Config = parse_config(config_source)

    # Construct a structured dictionary to return
    parsed_data = {
        "inputs": config.get("inputs", {}),
        "outputs": config.get("outputs", {}),
        "parameters": config.get("parameters", {}),
        "display_only": config.get("display_only", {}),
        "exec_function": config.get("exec_function", {}),
        "algorithm_folder_name": config.get("algorithm_folder_name", ""),
        "citations": config.get("citations", {"algorithm": {}})
    }

    # Returning a single structured dictionary
    return parsed_data

if __name__ == "__main__":
    # Use command-line argument if provided
    config_source = sys.argv[1] if len(sys.argv) > 1 else None

    # Get the parsed values as a dictionary
    parsed_data: dict[str, Any] = main(config_source)

    # Pretty print the parsed data for better readability
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(parsed_data)
