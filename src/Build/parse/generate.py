import os
# Importing parse function from parse.py
from parse import parse_config
from jinja2 import Environment, FileSystemLoader, select_autoescape

def preprocess_config(config):
    supported_input_types = {'Files', 'Radio', 'Number'}
    supported_output_types = {'Files'}

    inputs = [input_conf for input_conf in config.get('inputs', []) if input_conf['type'] in supported_input_types]
    outputs = [output_conf for output_conf in config.get('output', []) if output_conf['type'] in supported_output_types]
    exec_function = config.get('exec_function', {})

    return inputs, outputs, exec_function

def generate_gradio_app(template_path, inputs, outputs, exec_function):
    env = Environment(
        loader=FileSystemLoader(searchpath=os.path.dirname(template_path)),
        autoescape=select_autoescape(['j2'])
    )

    template = env.get_template(os.path.basename(template_path))

    gradio_app_code = template.render(inputs=inputs, outputs=outputs, exec_function=exec_function)
    return gradio_app_code

def main():
    print("Parsing config...")

    # inputs, outputs, exec_function = parse_config()
    config = parse_config()
    # inputs = config.get('inputs', [])
    # outputs = config.get('output', [])
    # exec_function = config.get('exec_function', {})
    inputs, outputs, exec_function = preprocess_config(config)

    template_path = "template.j2"
    # Generating the gradio algorithm+interface app dynamically
    gradio_app_code = generate_gradio_app(template_path, inputs, outputs, exec_function)
    # print(f"Inputs:", inputs)  
    # print(f"Outputs: {outputs}")  
    # print(f"Exec Function: {exec_function}")  

    with open('app.py', 'w') as f:
        f.write(gradio_app_code)
    print("app.py generated successfully!!")

if __name__ == "__main__":
    main()
