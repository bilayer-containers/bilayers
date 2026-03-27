from pathlib import Path
from typing import TypedDict, Any, Optional


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


class InterfaceInput(TypedDict):
    output_dir: Path
    inputs: dict[str, Input]
    outputs: dict[str, Output]
    parameters: dict[str, Parameter]
    display_only: Optional[dict[str, Parameter]]
    exec_function: ExecFunction
    citations: dict[str, Citations]
    docker_image: DockerImage
    cli_sequence: dict[str, dict[str, Any]]
