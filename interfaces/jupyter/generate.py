import os
from typing import Optional
from pathlib import Path

import nbformat as nbf
from jinja2 import Environment, FileSystemLoader, select_autoescape

from bilayers import project_path
from bilayers.parse import Citations, Input, Output, Parameter, ExecFunction, DockerImage
from bilayers.generate import generate_top_level_text

CITATION: Citations = {
    "name": "Jupyter",
    "doi": "10.1109/MCSE.2007.53",
    "license": "BSD 3-Clause",
    "description": "Interactive, code-driven documents for data analysis and visualization"
}

def generate_jupyter_notebook(
    template_dir: Path,
    template_name: str,
    inputs: dict[str, Input],
    outputs: dict[str, Output],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
    docker_image: DockerImage,
) -> nbf.NotebookNode:
    """
    Generates a Jupyter Notebook dynamically using Jinja2 templates.

    Args:
        template_dir (Path): Path to the Gradio template file's containing dir.
        template_name (str): name of the Gradio template file.
        inputs (dict[str, Input]): dictionary of input configurations.
        outputs (dict[str, Output]): dictionary of output configurations.
        parameters (dict[str, Parameter]): dictionary of parameter configurations.
        display_only (Optional[dict[str, Parameter]]): dictionary of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (dict[str, Citations]): Citations information.

    Returns:
        nbf.NotebookNode: The generated Jupyter Notebook object.
    """
    env = Environment(loader=FileSystemLoader(searchpath=str(template_dir)), autoescape=select_autoescape(["j2"]))

    def lower(text: str) -> str:
        return text.lower()

    def replace(text: str, old: str, new: str) -> str:
        return text.replace(old, new)

    def create_code_cell(content: str) -> nbf.NotebookNode:
        return nbf.v4.new_code_cell(content)

    def create_markdown_cell(content: str) -> nbf.NotebookNode:
        return nbf.v4.new_markdown_cell(content)

    template = env.get_template(template_name)
    notebook_content: str = template.render(inputs=inputs, outputs=outputs, parameters=parameters, display_only=display_only, exec_function=exec_function)

    title, full_description = generate_top_level_text(CITATION, citations, output_html=True)

    nb: nbf.NotebookNode = nbf.v4.new_notebook()

    # Add header markdown cells
    nb.cells.append(create_markdown_cell(f"# {title}"))
    nb.cells.append(create_markdown_cell(full_description))

    ########################################
    # Logic for Cell-1 in Jupyter Notebook
    ########################################
    # Create a hidden code cell for widget creation
    hidden_cell = create_code_cell(notebook_content)

    hidden_cell.metadata.jupyter = {"source_hidden": True}
    nb.cells.append(hidden_cell)

    ########################################
    # Logic for Cell-2 in Jupyter Notebook
    ########################################
    # Load and render the final validation template
    jupyter_final_validation_template_path = template_dir / "jupyter_final_validation_template.py.j2"
    jupyter_final_validation_template = env.get_template(os.path.basename(jupyter_final_validation_template_path))
    final_validation_code = jupyter_final_validation_template.render()
    # final validation code cell
    final_validation_code_cell = create_code_cell(final_validation_code)
    final_validation_code_cell.metadata.jupyter = {"source_hidden": True}
    # Append a new code cell with the final validation code to the notebook
    nb.cells.append(final_validation_code_cell)

    ########################################
    # Logic for Cell-3 in Jupyter Notebook
    ########################################
    # jupyter_shell_command_template_path
    jupyter_shell_command_template_path = template_dir / "jupyter_shell_command_template.py.j2"
    shell_command_template = env.get_template(os.path.basename(jupyter_shell_command_template_path))
    run_command_code: str = shell_command_template.render(cli_command=exec_function.get("cli_command", ""))
    # run command code cell
    run_command_code_cell = create_code_cell(run_command_code)
    run_command_code_cell.metadata.jupyter = {"source_hidden": True}
    # Append a new code cell with the run command code to the notebook
    nb.cells.append(run_command_code_cell)

    return nb

def generate(
    output_dir: Path,
    inputs: dict[str, Input],
    outputs: dict[str, Output],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
    docker_image: DockerImage,
):
    jupyter_template_path = project_path() / "interfaces/jupyter"

    jupyter_app_code = generate_jupyter_notebook(
        jupyter_template_path,
        "jupyter_template.py.j2",
        inputs,
        outputs,
        parameters,
        display_only,
        exec_function,
        citations,
        docker_image)

    jupyter_notebook_path = output_dir / "generated_notebook.ipynb"

    with open(jupyter_notebook_path, "w") as f:
        nbf.write(jupyter_app_code, f)

    print("Jupyter notebook saved as generated_notebook.ipynb")
