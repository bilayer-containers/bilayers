import os
# Importing parse function from parse.py
from parse import main as parse_config
from jinja2 import Environment, FileSystemLoader, select_autoescape

def preprocess_config(config):
    supported_input_types = {'Files', 'Radio', 'Number', 'Textbox', 'Checkbox'}
    supported_output_types = {'Files', 'Textbox', 'Image'}
    
    # section_mapping = {section['id']: section['label'] for section in config[0]}
    # # debugging what's there in section_mapping?
    # print(f"Section Mapping in generate.py: {section_mapping}")

    inputs = [input_conf for input_conf in config[1] if input_conf['type'] in supported_input_types]
    # print(f"Inputs in generate.py: {inputs}")

    outputs = [output_conf for output_conf in config[2] if output_conf['type'] in supported_output_types]

    exec_function = config[3]

    return inputs, outputs, exec_function


def generate_gradio_app(template_path, inputs, outputs, exec_function):
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

    print(f"Inputs: {inputs}")
    print(f"Outputs: {outputs}")
    print(f"Exec Function: {exec_function}")

    gradio_app_code = template.render(inputs=inputs, outputs=outputs, exec_function=exec_function)

    return gradio_app_code

def main():
    print("Parsing config...")

    # inputs, outputs, exec_function = parse_config()
    config = parse_config()
    
    inputs, outputs, exec_function = preprocess_config(config)

    template_path = "template.j2"

    # Generating the gradio algorithm+interface app dynamically
    gradio_app_code = generate_gradio_app(template_path, inputs, outputs, exec_function)

    with open('app.py', 'w') as f:
        f.write(gradio_app_code)
    print("app.py generated successfully!!")

if __name__ == "__main__":
    main()
