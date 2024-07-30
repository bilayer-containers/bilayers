# Displaying all the inouts in one widget
import os
import nbformat as nbf
from ipywidgets import widgets, VBox
from IPython.display import display
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

def create_widget_code(inputs, outputs, exec_function):    
    newest_code = f"""
from ipywidgets import widgets, VBox, HBox, Tab, Accordion
from IPython.display import display
import tempfile
import os

inputs = {inputs}
exec_function = {exec_function}

input_widgets = []
beginner_widgets = []
advanced_widgets = []

input_vars = []
# Appending args in cli_command
cli_command = []
cli_command.append(exec_function['cli_command'])

# Create widgets and corresponding descriptions and add Section-wise
for input_conf in inputs:
    if input_conf['type'] == 'Files' and input_conf['file_count'] == 'directory':
        input_widget = widgets.FileUpload(multiple=True)
    elif input_conf['type'] == 'Files' and input_conf['file_count'] == 'single':
        input_widget = widgets.FileUpload(multiple=False)
    elif input_conf['type'] == 'Radio':
        options = [opt['value'] for opt in input_conf['options']]
        input_widget = widgets.RadioButtons(options=options, value=input_conf['default'])
    elif input_conf['type'] == 'Number':
        default_value = input_conf['default']
        if default_value is None:
            input_widget = widgets.IntText(value=0)
        else:
            try:
                default_value = int(default_value)
            except ValueError:
                default_value = 0
            input_widget = widgets.IntText(value=default_value)
    elif input_conf['type'] == 'Textbox':
        input_widget = widgets.Textarea(value=input_conf['default'] if input_conf['default'] is not None else "")
    elif input_conf['type'] == 'Checkbox':
        input_widget = widgets.Checkbox(value=input_conf.get('value', False))

    # Description Label
    description_label = widgets.Label(value=input_conf.get('description', ''))

    # Add widget and description to accordion
    tab = Tab(children=[ HBox([widgets.Label(input_conf['label']), input_widget]), description_label ])
    tab.set_title(0, input_conf['label'])
    tab.set_title(1, "Description")

    # Append the corresponding cli_tag, widget to input_vars
    input_vars.append((input_conf['cli_tag'], input_widget))

    if input_conf['mode'] == 'beginner':
        beginner_widgets.append(tab)
    else:
        advanced_widgets.append(tab)    

acc = Accordion()
# Add beginner_widgets to the first section
acc.children = [VBox(beginner_widgets)]
acc.set_title(0, "Begginer's Section")
# Add advanced_widgets to the second section
acc.children = acc.children + (VBox(advanced_widgets),)
acc.set_title(1, "Advanced Section")

def construct_cli_command():
    cli_command = exec_function['cli_command']
    for cli_tag, widget in input_vars:
        if isinstance(widget, widgets.Checkbox):
            if widget.value == True:
                cli_command += f" {{cli_tag}}"
            else:
                continue
        elif isinstance(widget, widgets.Textarea):
            if widget.value == "":
                continue
            cli_command += f" {{cli_tag}} {{widget.value}}"
        elif isinstance(widget, widgets.RadioButtons):
            if widget.value != "None":
                cli_command += f" {{cli_tag}} {{widget.value}}"
            else:
                continue
        elif isinstance(widget, widgets.FileUpload):
            # Create a temporary directory and move all the input files there - as done in gradio
            temp_dir = tempfile.mkdtemp()
#             Since, widget.value is tuple
            for uploaded_file in widget.value:  
                file_content = uploaded_file['content']
                file_path = os.path.join(temp_dir, uploaded_file['name'])
                with open(file_path, 'wb') as f:
                    # Convert memoryview to bytes
                    f.write(file_content.tobytes())  
            # Update widget.value or cli_command as needed
            cli_command += f" {{cli_tag}} {{temp_dir}}"
        else:
            cli_command += f" {{cli_tag}} {{widget.value}}"
    return cli_command


def update_command(change):
    cli_command.value = construct_cli_command()

cli_command = widgets.Textarea(value=construct_cli_command(), description="CLI Command")

for _, widget in input_vars:
    widget.observe(update_command, names='value')

display(acc, cli_command)
"""

    return newest_code

def generate_jupyter_notebook(inputs, outputs, exec_function):
    nb = nbf.v4.new_notebook()
    
    # Create a markdown cell for instructions or say citations
    nb.cells.append(create_markdown_cell("## Set Variables and Run the cell"))

    # Create a hidden code cell for widget creation
    widget_code = create_widget_code(inputs, outputs, exec_function)
    # To hide the first cell
    hidden_cell = create_code_cell(widget_code)
    # hidden_cell.metadata.tags = ['hidden']
    # hidden_cell.metadata.hide_input = True
    # hidden_cell.metadata["jupyter"] = {"source_hidden": True}
    nb.cells.append(hidden_cell)

    nb.cells.append(create_code_cell(f"print({{cli_command.value}})"))

    run_command_cell = f"""
!{{cli_command.value}}
"""
    nb.cells.append(create_code_cell(run_command_cell))

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
