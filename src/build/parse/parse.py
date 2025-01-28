import yaml
import sys

def parse_config(config_path=None):
    if config_path is None:
        config_path = '../../../src/algorithms/classical_segmentation/config.yaml'
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main(config_path=None):

    config_path = sys.argv[1] if len(sys.argv) > 1 else None

    config = parse_config(config_path)

    inputs = config.get('inputs', [])

    outputs = config.get('outputs', [])

    parameters = config.get('parameters', [])

    display_only = config.get('display_only', [])

    exec_function = config.get('exec_function', {})

    algorithm_folder_name = config.get('algorithm_folder_name', None)

    citations = config.get('citations', [])

    return inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations

if __name__ == "__main__":

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations = main()
    print(f"Inputs: {inputs}")
    print(f"Outputs: {outputs}")
    print(f"Parameters: {parameters}")
    print(f"Display Only: {display_only}")
    print(f"Exec Function: {exec_function}")
    print(f"Folder Name: {algorithm_folder_name}")
    print(f"Citations: {citations}")