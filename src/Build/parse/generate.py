import os
# Importing parse function from parse.py
from parse import parse_config

def generate_gradio_app(inputs, outputs, exec_function):
    inputs_code = []
    for input_conf in inputs:
        print(f"Processing input: {input_conf}")  
        if input_conf['type'] == 'Files':
            inputs_code.append(f"gradio.Files(file_count='{input_conf['file_count']}', label='{input_conf['label']}')")
        elif input_conf['type'] == 'Radio':
            options = [opt['value'] for opt in input_conf['options']]
            inputs_code.append(f"gradio.Radio({options}, type='value', value='{options[0]}', label='{input_conf['label']}')")
        elif input_conf['type'] == 'Number':
            inputs_code.append(f"gradio.Number(value={input_conf['value']}, interactive={input_conf['interactive']}, label='{input_conf['label']}')")

    outputs_code = []
    for output_conf in outputs:
        print(f"Processing output: {output_conf}")  
        if output_conf['type'] == 'Files':
            outputs_code.append(f"gradio.File(label='{output_conf['label']}')")

    # Convert the lists to strings
    inputs_code_str = ",\n    ".join(inputs_code)
    outputs_code_str = ",\n    ".join(outputs_code)

    # Get the function name and script name
    function_name = exec_function['name']
    script_name = exec_function['script']


    gradio_app_code = f"""
import gradio
import skimage
import scipy
import numpy
import os
# Import the function from the script
from {script_name} import {function_name}

# Inputs to be shown in the GUI
inputs = [
    {inputs_code_str}
]

# Output to be shown in the GUI
output = [
    {outputs_code_str}
]

demo = gradio.Interface(
    fn=example_function, 
    inputs=inputs, 
    outputs=output,
    title="Simple ID objects"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000)
"""
    return gradio_app_code

def main():
    print("Parsing config...")

    # inputs, outputs, exec_function = parse_config()
    config = parse_config()
    inputs = config.get('inputs', [])
    outputs = config.get('output', [])
    exec_function = config.get('exec_function', {})

    # print(f"Inputs:", inputs)  
    # print(f"Outputs: {outputs}")  
    # print(f"Exec Function: {exec_function}")  

    # Generating Tool+Interface Specific Code
    gradio_app_code = generate_gradio_app(inputs, outputs, exec_function)
    with open('app.py', 'w') as f:
        f.write(gradio_app_code)
    print("app.py generated successfully!!")

if __name__ == "__main__":
    main()
