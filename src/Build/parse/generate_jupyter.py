import os
import nbformat as nbf
from ipywidgets import widgets, VBox
from IPython.display import display
import yaml
from parse import main as parse_config

def preprocess_config(config):
    supported_input_types = {'Files', 'Radio', 'Number', 'Textbox', 'Checkbox'}
    inputs = [input_conf for input_conf in config[1] if input_conf['type'] in supported_input_types]
    outputs = config[2]
    exec_function = config[3]
    return inputs, outputs, exec_function

def create_code_cell(content):
    return nbf.v4.new_code_cell(content)

def create_markdown_cell(content):
    return nbf.v4.new_markdown_cell(content)

def create_widget(inputs):
    
    input_widgets = []
    input_vars = []

    for input_conf in inputs:
        if input_conf['type'] == 'Files':
            input_widget = widgets.FileUpload(accept='directory')
        elif input_conf['type'] == 'Radio':
            options = [opt['value'] for opt in input_conf['options']]
            input_widget = widgets.RadioButtons(options=options, value=input_conf['default'])
        elif input_conf['type'] == 'Number':
            input_widget = widgets.IntText(value=input_conf['default'])
        elif input_conf['type'] == 'Textbox':
            input_widget = widgets.Textarea(value=input_conf['default'])
        elif input_conf['type'] == 'Checkbox':
            input_widget = widgets.Checkbox(value=input_conf.get('value', False))

        input_widgets.append(widgets.HBox([widgets.Label(input_conf['label']), input_widget]))
        input_vars.append((input_conf['cli_tag'], input_widget))

    return display(VBox(input_widgets))



def generate_jupyter_notebook(inputs, outputs, exec_function):
    nb = nbf.v4.new_notebook()
    
    # Create a markdown cell for labels
    nb.cells.append(create_markdown_cell("## Set Variables and Run the cell"))

    # Create a code cell for setting variables
    # code = create_widget(inputs)
    get_direct_inputs = create_widget(inputs)

    code = f"""
from ipywidgets import widgets , VBox, HBox  
from IPython.display import display

inputs = {inputs}

input_widgets = []
input_vars = []

for input_conf in inputs:
    if input_conf['type'] == 'Files':
        input_widget = widgets.FileUpload(accept='directory')
    elif input_conf['type'] == 'Radio':
        options = [opt['value'] for opt in input_conf['options']]
        input_widget = widgets.RadioButtons(options=options, value=input_conf['default'])
    elif input_conf['type'] == 'Number':
        input_widget = widgets.IntText(value=input_conf['default'])
    elif input_conf['type'] == 'Textbox':
        input_widget = widgets.Textarea(value=input_conf['default'])
    elif input_conf['type'] == 'Checkbox':
        input_widget = widgets.Checkbox(value=input_conf.get('value', False))

    input_widgets.append(widgets.HBox([widgets.Label(input_conf['label']), input_widget]))
    input_vars.append((input_conf['cli_tag'], input_widget))

display(VBox(input_widgets))
"""

    nb.cells.append(create_code_cell(code))
    # nb.cells.append(create_code_cell(get_direct_inputs))
    
    return nb

def main():
    print("Parsing config...")

    config = parse_config()
    inputs, outputs, exec_function = preprocess_config(config)

    jupyter_app_code = generate_jupyter_notebook(inputs, outputs, exec_function)
    
    # Save the notebook
    notebook_path = "generated_notebook.ipynb"
    with open(notebook_path, "w") as f:
        nbf.write(jupyter_app_code, f)
    
    print(f"Jupyter notebook saved at {notebook_path}")

if __name__ == "__main__":
    main()
