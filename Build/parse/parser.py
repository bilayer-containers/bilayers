import yaml

def parse_config(config_path="../../Algorithms/threshold/config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():

    config = parse_config()
    
    inputs = config.get('inputs', [])
    output = config.get('output', [])
    
    # Exec function whole logic from threshold.py instead of just the function name
    exec_function = config.get('exec_function', {})
    return inputs, output, exec_function

if __name__ == "__main__":
    inputs, outputs, exec_function = main()
    print(f"Inputs: {inputs}")
    print(f"Outputs: {outputs}")
    print(f"Exec Function: {exec_function}")

    