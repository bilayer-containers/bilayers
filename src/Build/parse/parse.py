import yaml
import sys

def parse_config(config_path=None):
    if config_path is None:
        config_path = '../../../src/Algorithms/threshold/config.yaml'
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main(config_path=None):

    config_path = sys.argv[1] if len(sys.argv) > 1 else None

    config = parse_config(config_path)


    parameters = config.get('parameters', [])
    
    outputs = config.get('outputs', [])
    
    # Exec function whole logic from threshold.py instead of just the function name
    exec_function = config.get('exec_function', {})

    folder_name = config.get('folder_name', None)

    citations = config.get('citations', [])

    return parameters, outputs, exec_function, folder_name, citations

if __name__ == "__main__":

    parameters, outputs, exec_function, folder_name, citations = main()
    print(f"Parameters: {parameters}")
    print(f"Outputs: {outputs}")
    print(f"Exec Function: {exec_function}")
    print(f"Folder Name: {folder_name}")
    print(f"Citations: {citations}")

    