from typing import Optional
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from bilayers import project_path
from bilayers.parse import Citations, Input, Output, Parameter, ExecFunction, DockerImage
from bilayers.generate import generate_top_level_text


CITATION: Citations = {
    "name": "Gradio",
    "doi": "10.48550/arXiv.190602569",
    "license": "Apache License 2.0",
    "description": "A simple web interface for deploying machine learning models"
}

def generate_gradio_app(
    template_dir: Path,
    template_name: str,
    inputs: dict[str, Input],
    outputs: dict[str, Output],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
    docker_image: DockerImage,
    cli_sequence: dict[str, dict],
) -> str:
    """
    Generates a Gradio application dynamically using Jinja2 templates.

    Args:
        template_dir (Path): Path to the Gradio template file's containing dir.
        template_name (str): name of the Gradio template file.
        inputs (dict[str, Input]): dictionary of input configurations.
        outputs (dict[str, Output]): dictionary of output configurations.
        parameters (dict[str, Parameter]): dictionary of parameter configurations.
        display_only (Optional[dict[str, Parameter]]): dictionary of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (dict[str, Citations]): Citations information.
        cli_sequence (dict[str, dict]): Pre-ordered sequence of CLI arguments.

    Returns:
        str: The rendered Gradio application code.
    """
    env = Environment(loader=FileSystemLoader(searchpath=str(template_dir)), autoescape=select_autoescape(["j2"]))

    def lower(text: str) -> str:
        return text.lower()

    def replace(text: str, old: str, new: str) -> str:
        return text.replace(old, new)

    env.filters["lower"] = lower
    env.filters["replace"] = replace

    template = env.get_template(template_name)

    title, full_description = generate_top_level_text(CITATION, citations, output_html=False)

    split_parameters = {}
    parameters_flat = {}

    for paramkey, paramvalue in parameters.items():
        assert "type" in paramvalue and "default" in paramvalue and "label" in paramvalue
        if paramvalue["type"] in ["float", "integer"] and str(paramvalue["default"]) in ["None", "False"]:
            # "Set a value?" toggle
            bool_param = dict(paramvalue)
            bool_param["name"] = f"set_{paramkey}"
            bool_param["type"] = "checkbox"
            bool_param["default"] = False
            bool_param["cli_tag"] = ""
            bool_param["optional"] = True
            newlabel = paramvalue["label"][0].lower() + paramvalue["label"][1:]
            bool_param["label"] = f"Set a value for {newlabel}?"
            bool_param["description"] = paramvalue.get("description", "")

            # Actual number input (hidden unless checkbox is ticked)
            num_param = dict(paramvalue)
            num_param["name"] = paramkey
            num_param["default"] = 0
            num_param["optional"] = True

            split_parameters[paramkey] = {
                f"set_{paramkey}": bool_param,
                paramkey: num_param,
            }
            parameters_flat[f"set_{paramkey}"] = bool_param
            parameters_flat[paramkey] = num_param
        else:
            parameters_flat[paramkey] = paramvalue

    gradio_app_code: str = template.render(
        inputs=inputs,
        outputs=outputs,
        parameters=parameters_flat,
        split_parameters=split_parameters,
        display_only=display_only,
        exec_function=exec_function,
        title=title,
        description=full_description,
        cli_sequence=list(cli_sequence.values()),
    )

    return gradio_app_code

def generate(
    output_dir: Path,
    inputs: dict[str, Input],
    outputs: dict[str, Output],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
    docker_image: DockerImage,
    cli_sequence: dict[str, dict],
):
    gradio_template_path = project_path() / "interfaces/gradio"

    gradio_app_code = generate_gradio_app(
        gradio_template_path,
        "gradio_template.py.j2",
        inputs,
        outputs,
        parameters,
        display_only,
        exec_function,
        citations,
        docker_image,
        cli_sequence)

    gradio_app_path = output_dir / "app.py"

    with open(gradio_app_path, "w") as f:
        f.write(gradio_app_code)

    print("app.py generated successfully!!")
