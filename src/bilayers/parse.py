import yaml
from typing import TypedDict, Any, Optional, Union
from pathlib import Path


class Citations(TypedDict):
    name: str
    doi: str
    license: str
    description: str


class HiddenArgs(TypedDict, total=False):
    cli_tag: str
    value: str
    append_value: bool
    cli_order: int

class DockerImage(TypedDict):
    org: str
    name: str
    tag: str
    platform: str

class ExecFunction(TypedDict):
    name: str
    cli_command: str
    hidden_args: Optional[dict[str, HiddenArgs]]


class InputOutputBase(TypedDict, total=False):
    name: str
    type: str
    label: str
    subtype: list[str]  # w.r.t type == image
    description: str
    cli_tag: Optional[str]
    cli_order: Optional[int]
    default: str
    optional: bool
    unique_string: list[str]
    format: list[str]
    folder_name: str
    file_count: str
    section_id: str
    mode: str
    depth: Optional[bool]  # w.r.t type == image
    timepoints: Optional[bool]  # w.r.t type == image
    tiled: Optional[bool]  # w.r.t type == image
    pyramidal: Optional[bool]  # w.r.t type == image

class Input(InputOutputBase):
    pass

class Output(InputOutputBase):
    pass
class Parameter(TypedDict, total=False):
    name: str
    type: str
    label: str
    description: str
    default: Any
    cli_tag: Optional[str]
    cli_order: Optional[int]
    optional: bool
    section_id: str
    mode: str
    options: Optional[list[dict[str, str]]]  # w.r.t type == radio, dropdown
    output_dir_set: Optional[bool]  # w.r.t type == textbox
    interactive: Optional[bool]
    append_value: Optional[bool]  # w.r.t type == checkbox
    multiselect: Optional[bool]  # w.r.t type == dropdown


class Config(TypedDict):
    citations: dict[str, Citations]
    algorithm_folder_name: str
    exec_function: ExecFunction
    inputs: dict[str, Input]
    outputs: dict[str, Output]
    parameters: dict[str, Parameter]
    display_only: Optional[dict[str, Parameter]]
    docker_image: DockerImage


def load_config(config_path: Union[str, Path]):
    # even if already type Path, convert
    # to stop the type checker from complaining
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config


def parse_config(config_path: Union[str, Path]) -> Config:
    """
    Parses a YAML configuration file.

    Args:
        config_path (Optional[str | Path]): Path to the config file. Defaults to None.

    Returns:
        Config: A structured dictionary containing parsed YAML data.
    """
    config = load_config(config_path)
    # Convert lists to dictionaries using "name" as key
    config["inputs"] = {item["name"]: item for item in config.get("inputs", [])} if isinstance(config.get("inputs"), list) else {}
    config["outputs"] = {item["name"]: item for item in config.get("outputs", [])} if isinstance(config.get("outputs"), list) else {}
    config["parameters"] = {item["name"]: item for item in config.get("parameters", [])} if isinstance(config.get("parameters"), list) else {}
    config["display_only"] = {item["name"]: item for item in config.get("display_only", [])} if isinstance(config.get("display_only"), list) else {}

    config["citations"] = {item["name"]: item for item in config.get("citations", [])} if isinstance(config.get("citations"), list) else {}

    # Convert hidden_args to dictionary
    hidden_args = config["exec_function"].get("hidden_args", [])
    if isinstance(hidden_args, list):
        config["exec_function"]["hidden_args"] = {arg["cli_tag"]: arg for arg in hidden_args}
    else:
        config["exec_function"]["hidden_args"] = {}

    return config


def safe_parse_config(
    config_path: Union[str, Path],
) -> tuple[
        dict[str, Input],
        dict[str, Output],
        dict[str, Parameter],
        Optional[dict[str, Parameter]],
        ExecFunction,
        str,
        dict[str, Citations],
        DockerImage
    ]:
    """
    Loads the configuration and extracts necessary information.

    Args:
        config_path (Optional[str]): Path to the configuration file.

    Returns:
        tuple containing parsed configuration data.
    """
    config: Config = parse_config(config_path)

    inputs: dict[str, Input] = config.get("inputs", {})

    outputs: dict[str, Output] = config.get("outputs", {})

    parameters: dict[str, Parameter] = config.get("parameters", {})

    display_only: Optional[dict[str, Parameter]] = config.get("display_only", {})

    exec_function: ExecFunction = config.get("exec_function", {})
    exec_function.setdefault("name", "")
    exec_function.setdefault("cli_command", "")
    exec_function.setdefault("hidden_args", {})

    # TODO: blank algorithm_folder_name is unsafe because we unconditionally create folders with it downstream
    algorithm_folder_name: str = config.get("algorithm_folder_name", "")

    citations: dict[str, Citations] = config.get("citations", {})

    # Since, we are sure that docker_image key exists in the config, we can safely use it.
    docker_image: DockerImage = config["docker_image"]

    return inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image
