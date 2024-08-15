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

    folder_name = config.get('folder_name', None)

    citations = config.get('citations', [])

    return sections, inputs, outputs, exec_function, folder_name, citations

if __name__ == "__main__":

    sections, inputs, outputs, exec_function, folder_name, citations = main()
    print(f"Sections: {sections}")
    print(f"Inputs: {inputs}")
    print(f"Outputs: {outputs}")
    print(f"Exec Function: {exec_function}")
    print(f"Folder Name: {folder_name}")
    print(f"Citations: {citations}")

    