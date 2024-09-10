import os
import sys
# Importing parse function from parse.py
from parse import main as parse_config
from jinja2 import Environment, FileSystemLoader, select_autoescape
import nbformat as nbf 
import ipywidgets as widgets
from IPython.display import display, HTML, FileLink
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path


def generate_gradio_app(template_path, parameters, display_only, results, exec_function, citations):
    env = Environment(
        loader=FileSystemLoader(searchpath=os.path.dirname(template_path)),
        autoescape=select_autoescape(['j2'])
    )

    def lower(text):
        return text.lower()

    def replace(text, old, new):
        return text.replace(old, new)

    env.filters['lower'] = lower
    env.filters['replace'] = replace

    template = env.get_template(os.path.basename(template_path))

    gradio_app_code = template.render(parameters=parameters, display_only=display_only, results=results, exec_function=exec_function, citations=citations)

    return gradio_app_code


def generate_jupyter_notebook(template_path, parameters, display_only, results, exec_function, citations):
    env = Environment(
        loader=FileSystemLoader(searchpath=os.path.dirname(template_path)),
        autoescape=select_autoescape(['j2'])
    )

    def lower(text):
        return text.lower()

    def replace(text, old, new):
        return text.replace(old, new)
    
    def create_code_cell(content):
        return nbf.v4.new_code_cell(content)

    def create_markdown_cell(content):
        return nbf.v4.new_markdown_cell(content)

    template = env.get_template(os.path.basename(template_path))
    print("To check the type of parameters: ", type(parameters))
    notebook_content = template.render(parameters=parameters, display_only=display_only, results=results, exec_function=exec_function)

    DEFAULT_CITATIONS = {
        "Bilayers": [
            {
                "name" : "Bilayers",
                "license" : "xxxx",
                "description" : "GUI interfaces for deep learning-based cell segmentation algorithms"
            },
        ],
        "Jupyter": [
            {
                "name" : "Jupyter",
                "doi" : "10.1109/MCSE.2007.53",
                "description" : "Interactive, code-driven documents for data analysis and visualization"
            },
        ],
    }

    nb = nbf.v4.new_notebook()
    
    # Create a markdown cell for instructions or say citations
    nb.cells.append(create_markdown_cell("## Set Variables and Run the cell"))

    for citation in DEFAULT_CITATIONS['Bilayers']:
        citation_cell = f"- {citation['name']} : {citation['license']} --> {citation['description']}\n"

    for citation in DEFAULT_CITATIONS['Jupyter']:
        citation_cell += f"- {citation['name']} : {citation['doi']} --> {citation['description']}\n"

    for citation in citations['Algorithm']:
        citation_cell += f"- {citation['name']} : {citation['doi']} --> {citation['description']}\n"

    # Add a markdown cell with the formatted citations
    nb.cells.append(create_markdown_cell(citation_cell))

    # Create a hidden code cell for widget creation
    hidden_cell = create_code_cell(notebook_content)
    
    hidden_cell.metadata.jupyter = {"source_hidden": True}
    nb.cells.append(hidden_cell)

    nb.cells.append(create_code_cell(f"print({{cli_command.value}})"))
    
    # jupyter_shell_command_template_path
    jupyter_shell_command_template_path = "jupyter_shell_command_template.py.j2"
    shell_command_template = env.get_template(os.path.basename(jupyter_shell_command_template_path))
    run_command_cell = shell_command_template.render(cli_command=exec_function['cli_command'])
    
    # Append the try-except cell to the notebook
    nb.cells.append(create_code_cell(run_command_cell))

    return nb
def main():
    print("Parsing config...")

    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = None

    parameters, display_only, results, exec_function, folder_name, citations = parse_config(config_path)


    ########################################
    # Logic for generating Gradio App
    ########################################

    folderA = "generated_folders"
    folderB = folder_name
    # CreAate Directory if they don't exist
    os.makedirs(os.path.join(folderA, folderB), exist_ok=True)

    # Template path for the Gradio app
    gradio_template_path = "gradio_template.py.j2"

    # Generating the gradio algorithm+interface app dynamically
    gradio_app_code = generate_gradio_app(gradio_template_path, parameters, display_only, results, exec_function, citations)

    # Join folders and file name
    gradio_app_path = os.path.join(folderA, folderB, 'app.py')

    # Generating Gradio app file dynamically
    with open(gradio_app_path, 'w') as f:
        f.write(gradio_app_code)
    print("app.py generated successfully!!")


    ################################################
    # Logic for generating Jupyter Notebook
    ################################################

    folderA = "generated_folders"
    folderB = folder_name
    print("Folder Name: ", folderB)
    # Create Directory if they don't exist
    os.makedirs(os.path.join(folderA, folderB), exist_ok=True)

    # Template path for the Jupyter Notebook
    jupyter_template_path = "jupyter_template.py.j2"

    # Generating Jupyter Notebook file dynamically
    jupyter_app_code = generate_jupyter_notebook(jupyter_template_path, parameters, display_only, results, exec_function, citations)

    # Join folders and file name
    jupyter_notebook_path = os.path.join(folderA, folderB, 'generated_notebook.ipynb')
    
    with open(jupyter_notebook_path, "w") as f:
        nbf.write(jupyter_app_code, f)
    print("Jupyter notebook saved at generated_notebook.ipynb")


if __name__ == "__main__":
    main()
