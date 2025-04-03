import os
import sys


# Importing parse function from parse.py
from parse import main as parse_config  # type: ignore
from jinja2 import Environment, FileSystemLoader, select_autoescape
import nbformat as nbf

# Import TypedDict definitions from parse.py
from parse import InputOutput, Parameter, ExecFunction, Citations  # type: ignore


def generate_gradio_app(
    template_path: str,
    inputs: dict[str, InputOutput],
    outputs: dict[str, InputOutput],
    parameters: dict[str, Parameter],
    display_only: dict[str, Parameter] | None,
    exec_function: ExecFunction,
    citations: Citations,
) -> str:
    """
    Generates a Gradio application dynamically using Jinja2 templates.

    Args:
        template_path (str): Path to the Gradio template file.
        inputs (dict[str, InputOutput]): dictionary of input configurations.
        outputs (dict[str, InputOutput]): dictionary of output configurations.
        parameters (dict[str, Parameter]): dictionary of parameter configurations.
        display_only (dict[str, Parameter] | None): dictionary of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (Citations): Citations information.

    Returns:
        str: The rendered Gradio application code.
    """
    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)), autoescape=select_autoescape(["j2"]))

    def lower(text: str) -> str:
        return text.lower()

    def replace(text: str, old: str, new: str) -> str:
        return text.replace(old, new)

    env.filters["lower"] = lower
    env.filters["replace"] = replace

    template = env.get_template(os.path.basename(template_path))

    gradio_app_code: str = template.render(
        inputs=inputs, outputs=outputs, parameters=parameters, display_only=display_only, exec_function=exec_function, citations=citations
    )

    return gradio_app_code


def generate_jupyter_notebook(
    template_path: str,
    inputs: dict[str, InputOutput],
    outputs: dict[str, InputOutput],
    parameters: dict[str, Parameter],
    display_only: dict[str, Parameter] | None,
    exec_function: ExecFunction,
    citations: Citations,
) -> nbf.NotebookNode:
    """
    Generates a Jupyter Notebook dynamically using Jinja2 templates.

    Args:
        template_path (str): Path to the Jupyter Notebook template file.
        inputs (dict[str, InputOutput]): dictionary of input configurations.
        outputs (dict[str, InputOutput]): dictionary of output configurations.
        parameters (dict[str, Parameter]): dictionary of parameter configurations.
        display_only (dict[str, Parameter] | None): dictionary of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (Citations): Citations information.

    Returns:
        nbf.NotebookNode: The generated Jupyter Notebook object.
    """
    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)), autoescape=select_autoescape(["j2"]))

    def lower(text: str) -> str:
        return text.lower()

    def replace(text: str, old: str, new: str) -> str:
        return text.replace(old, new)

    def create_code_cell(content: str) -> nbf.NotebookNode:
        return nbf.v4.new_code_cell(content)

    def create_markdown_cell(content: str) -> nbf.NotebookNode:
        return nbf.v4.new_markdown_cell(content)

    template = env.get_template(os.path.basename(template_path))
    notebook_content: str = template.render(inputs=inputs, outputs=outputs, parameters=parameters, display_only=display_only, exec_function=exec_function)

    DEFAULT_CITATIONS: dict[str, list[dict[str, str]]] = {
        "Bilayers": [
            {"name": "Bilayers", "license": "BSD 3-Clause", "description": "A Container Specification and CI/CD  built for whole-community support"},
        ],
        "Jupyter": [
            {
                "name": "Jupyter",
                "doi": "10.1109/MCSE.2007.53",
                "license": "BSD 3-Clause",
                "description": "Interactive, code-driven documents for data analysis and visualization",
            },
        ],
    }

    nb: nbf.NotebookNode = nbf.v4.new_notebook()

    # Create a markdown cell for instructions or say citations
    nb.cells.append(create_markdown_cell("## Set Variables and Run the cell"))

    citation_cell: str = ""
    for citation in citations.get("algorithm", {}).values():
        citation_cell += (
            f"- {citation.get('name', 'Unknown Name')} under {citation.get('license', 'Unknown')} License "
            f": {citation.get('doi', 'No Description Available')} --> {citation.get('description', 'No Description Available')}\n"
        )
    for citation in DEFAULT_CITATIONS["Jupyter"]:
        citation_cell += (
            f"- {citation.get('name', 'Unknown Name')} under {citation.get('license', 'Unknown')} License "
            f": {citation.get('doi', 'No Description Available')} --> {citation.get('description', 'No Description Available')}\n"
        )

    for citation in DEFAULT_CITATIONS["Bilayers"]:
        citation_cell += (
            f"- {citation.get('name', 'Unknown Name')} : {citation.get('license', 'Unknown License')} "
            f" --> {citation.get('description', 'No Description Available')}\n"
        )

    # Add a markdown cell with the formatted citations
    nb.cells.append(create_markdown_cell(citation_cell))

    # Create a hidden code cell for widget creation
    hidden_cell = create_code_cell(notebook_content)

    hidden_cell.metadata.jupyter = {"source_hidden": True}
    nb.cells.append(hidden_cell)

    nb.cells.append(create_code_cell("print({cli_command.value})"))

    # jupyter_shell_command_template_path
    jupyter_shell_command_template_path = "jupyter_shell_command_template.py.j2"
    shell_command_template = env.get_template(os.path.basename(jupyter_shell_command_template_path))
    run_command_cell: str = shell_command_template.render(cli_command=exec_function.get("cli_command", ""))

    # Append the try-except cell to the notebook
    nb.cells.append(create_code_cell(run_command_cell))

    return nb


def main() -> None:
    """Main function to parse config and generate Gradio and Jupyter notebook files."""
    print("Parsing config...")

    if len(sys.argv) > 1:
        config_path: str | None = sys.argv[1]
    else:
        config_path = None

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations = parse_config(config_path)

    folderA: str = "generated_folders"
    folderB: str = algorithm_folder_name
    # Create Directory if they don't exist
    os.makedirs(os.path.join(folderA, folderB), exist_ok=True)

    ########################################
    # Logic for generating Gradio App
    ########################################

    # Template path for the Gradio app
    gradio_template_path: str = "gradio_template.py.j2"

    # Generating the gradio algorithm+interface app dynamically
    gradio_app_code: str = generate_gradio_app(gradio_template_path, inputs, outputs, parameters, display_only, exec_function, citations)

    # Join folders and file name
    gradio_app_path: str = os.path.join(folderA, folderB, "app.py")

    # Generating Gradio app file dynamically
    with open(gradio_app_path, "w") as f:
        f.write(gradio_app_code)
    print("app.py generated successfully!!")

    ################################################
    # Logic for generating Jupyter Notebook
    ################################################

    # Template path for the Jupyter Notebook
    jupyter_template_path: str = "jupyter_template.py.j2"

    # Generating Jupyter Notebook file dynamically
    jupyter_app_code: nbf.NotebookNode = generate_jupyter_notebook(jupyter_template_path, inputs, outputs, parameters, display_only, exec_function, citations)

    # Join folders and file name
    jupyter_notebook_path: str = os.path.join(folderA, folderB, "generated_notebook.ipynb")

    with open(jupyter_notebook_path, "w") as f:
        nbf.write(jupyter_app_code, f)
    print("Jupyter notebook saved at generated_notebook.ipynb")


if __name__ == "__main__":
    main()
