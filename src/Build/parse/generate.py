import os
# Importing parse function from parse.py
from parse import main as parse_config
from jinja2 import Environment, FileSystemLoader, select_autoescape
import nbformat as nbf 
import ipywidgets as widgets
from IPython.display import display, HTML

def preprocess_config(config):
    supported_input_types = {'Files', 'Radio', 'Number', 'Textbox', 'Checkbox', 'Float', 'Integer'}
    supported_output_types = {'Files', 'Textbox', 'Image'}
    
    # section_mapping = {section['id']: section['label'] for section in config[0]}
    # # debugging what's there in section_mapping?
    # print(f"Section Mapping in generate.py: {section_mapping}")

    inputs = [input_conf for input_conf in config[1] if input_conf['type'] in supported_input_types]
    # print(f"Inputs in generate.py: {inputs}")

    outputs = [output_conf for output_conf in config[2] if output_conf['type'] in supported_output_types]

    exec_function = config[3]

    folder_name = config[4]

    citations = config[5]

    return inputs, outputs, exec_function, folder_name, citations


def generate_gradio_app(template_path, inputs, outputs, exec_function, citations):
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

    gradio_app_code = template.render(inputs=inputs, outputs=outputs, exec_function=exec_function, citations=citations)

    return gradio_app_code


def generate_jupyter_notebook(template_path, inputs, outputs, exec_function, citations):
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
    print("To check the type of inputs: ", type(inputs))
    notebook_content = template.render(inputs=inputs, outputs=outputs, exec_function=exec_function)

    nb = nbf.v4.new_notebook()
    
    # Create a markdown cell for instructions or say citations
    nb.cells.append(create_markdown_cell("## Set Variables and Run the cell"))

    citation_cell = "### Please use the following citations while using Bilayers - JupyterNotebook Interface!\n"
    for citation in citations['Bilayers']:
        citation_cell += f"- {citation['name']} : {citation['license']} --> {citation['description']}\n"

    for citation in citations['Jupyter']:
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


    run_command_cell = f"""
import subprocess
import nbformat as nbf
from IPython.core.getipython import get_ipython
try:
    res = subprocess.run(cli_command.value, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    !{{cli_command.value}}

except Exception as e:
    error_message = str(e)
    # print(f"Error occurred: {{error_message}}")
    error_cell = nbf.v4.new_code_cell(f"# Error Details: {{error_message}}")

    ####################
    # Display the error cell
    shell = get_ipython()
    shell.payload_manager.write_payload(dict(
    source='set_next_input',
    text=error_cell['source'],
    replace=False), single=False)
"""
    
    # Append the try-except cell to the notebook
    nb.cells.append(create_code_cell(run_command_cell))

    return nb
def main():
    print("Parsing config...")

    # inputs, outputs, exec_function = parse_config()
    config = parse_config()
    
    inputs, outputs, exec_function, folder_name, citations = preprocess_config(config)

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
    gradio_app_code = generate_gradio_app(gradio_template_path, inputs, outputs, exec_function, citations)

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
    # CreAate Directory if they don't exist
    os.makedirs(os.path.join(folderA, folderB), exist_ok=True)

    # Template path for the Jupyter Notebook
    jupyter_template_path = "jupyter_template.py.j2"

    # Generating Jupyter Notebook file dynamically
    jupyter_app_code = generate_jupyter_notebook(jupyter_template_path, inputs, outputs, exec_function, citations)

    # Join folders and file name
    jupyter_notebook_path = os.path.join(folderA, folderB, 'generated_notebook.ipynb')
    
    with open(jupyter_notebook_path, "w") as f:
        nbf.write(jupyter_app_code, f)
    print("Jupyter notebook saved at generated_notebook.ipynb")


if __name__ == "__main__":
    main()
