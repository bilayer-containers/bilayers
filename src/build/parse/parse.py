import yaml
import sys

def parse_config(config_path=None):
    if config_path is None:
        config_path = '../../../src/algorithms/threshold/config.yaml'
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main(config_path=None):

    config_path = sys.argv[1] if len(sys.argv) > 1 else None

    config = parse_config(config_path)

    parameters = config.get('parameters', [])

    display_only = config.get('display_only', [])

    results = config.get('results', [])

    # Exec function whole logic from threshold.py instead of just the function name
    exec_function = config.get('exec_function', {})

    algorithm_folder_name = config.get('algorithm_folder_name', None)

    citations = config.get('citations', [])

    return parameters, display_only, results, exec_function, algorithm_folder_name, citations

if __name__ == "__main__":

    parameters, display_only, results, exec_function, algorithm_folder_name, citations = main()
    print(f"Parameters: {parameters}")
    print(f"Display Only: {display_only}")
    print(f"Results: {results}")
    print(f"Exec Function: {exec_function}")
    print(f"Folder Name: {algorithm_folder_name}")
    print(f"Citations: {citations}")
