import yaml

def parse_config(config_path="../../../src/Algorithms/cellpose/config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():

    config = parse_config()

    sections = config.get('sections', [])

    inputs = config.get('inputs', [])
    
    outputs = config.get('outputs', [])
    
    # Exec function whole logic from threshold.py instead of just the function name
    exec_function = config.get('exec_function', {})
    return sections, inputs, outputs, exec_function

if __name__ == "__main__":
    # sections, inputs, outputs, exec_function = main()

    sections, inputs, outputs, exec_function = main()
    print(f"Sections: {sections}")
    print(f"Inputs: {inputs}")
    print(f"Outputs: {outputs}")
    print(f"Exec Function: {exec_function}")

    