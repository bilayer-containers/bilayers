
from typing import Optional
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from bilayers import project_path
from bilayers.parse import Citations, Input, Output, Parameter, ExecFunction, DockerImage
from bilayers.generate import generate_top_level_text


CITATION: Citations = {
    "name": "Streamlit",
    "doi": "",
    "license": "Apache License 2.0",
    "description": "A library for easily creating custom web interfaces",
}

def generate_streamlit_app(
    template_dir: Path,
    template_name: str,
    inputs: dict[str, Input],
    outputs: dict[str, Output],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
    docker_image: DockerImage,
) -> str:
    """
    Generates a Streamlit application dynamically using Jinja2 templates.

    Args:
        template_dir (Path): Path to the Streamlit template file's containing dir.
        template_name (str): name of the Streamlit template file.
        inputs (dict[str, Input]): dictionary of input configurations.
        outputs (dict[str, Output]): dictionary of output configurations.
        parameters (dict[str, Parameter]): dictionary of parameter configurations.
        display_only (Optional[dict[str, Parameter]]): dictionary of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (dict[str, Citations]): Citations information.

    Returns:
        str: The rendered Streamlit application code.
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

    streamlit_app_code: str = template.render(
        inputs=inputs, outputs=outputs, parameters=parameters, display_only=display_only, exec_function=exec_function, title=title, description=full_description
    )

    return streamlit_app_code


def generate(
    output_dir: Path,
    inputs: dict[str, Input],
    outputs: dict[str, Output],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
    docker_image: DockerImage
):
    streamlit_template_path = project_path() / "interfaces/streamlit"

    streamlit_app_code = generate_streamlit_app(
        streamlit_template_path,
        "streamlit_template.py.j2",
        inputs,
        outputs,
        parameters,
        display_only,
        exec_function,
        citations, 
        docker_image)


    streamlit_app_path = output_dir / "streamlit_app.py"

    with open(streamlit_app_path, "w") as f:
        f.write(streamlit_app_code)
    print("streamlit_app.py generated successfully!!")
