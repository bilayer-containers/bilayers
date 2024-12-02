import os
import subprocess
import sys
from dummy_parse import parse_config  # Import parse.py for spec parsing

def build_cli_command(exec_function, parameters):
    """
    Build the CLI command dynamically from parameters.
    
    Args:
        exec_function (str): Base command (e.g., "python -m cellpose")
        parameters (list): List of parameter dictionaries from the spec file

    Returns:
        str: Complete CLI command
    """
    cli_args = [exec_function]
    
    for param in parameters:
        cli_tag = param.get("cli_tag")
        value = param.get("default")
        optional = param.get("optional", True)
        type = param.get("type")

        if type == "checkbox":
            append_value = param.get("append_value", False)
            if append_value and value:
                cli_args.append(f"{cli_tag} {value}")
            elif append_value and not value:
                cli_args.append(cli_tag)
            else:
                if value:
                    cli_args.append(cli_tag)
        elif type == "files":
            value = param.get("folder_name")
            cli_args.append(f"{cli_tag} {value}")
        else:
            cli_args.append(f"{cli_tag} {value}")
    
    return " ".join(cli_args)

def run_segmentation(command):
    """
    Execute the segmentation command
    
    Args:
        command (str): The CLI command to execute
    """
    print(f"Executing command: {command}")
    subprocess.run(command, shell=True, check=True)
    print("Segmentation completed successfully!")

# Not using as of now! (Ignore)
def pack_outputs_to_docker(output_dir, docker_image_name="segmentation_outputs"):
    """
    Create a Docker image with the segmentation outputs.
    """
    dockerfile_content = f"""
    FROM python:3.9-slim
    COPY {output_dir} /outputs
    """
    dockerfile_path = os.path.join(output_dir, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content)

    print("...Building Docker image with outputs...")
    subprocess.run(["docker", "build", "-t", docker_image_name, output_dir], check=True)
    print(f"Docker image '{docker_image_name}' built successfully!!")

def main():
    # Step 1: Parse the spec file
    config_path = sys.argv[1] if len(sys.argv) > 1 else "src/algorithms/cellpose_input_output/config.yaml"
    config = parse_config(config_path)

    # Step 2: Extract exec_function and parameters
    exec_function = config.get("exec_function", {}).get("cli_command")
    parameters = config.get("parameters")
    outputs = config.get("outputs")

    # Step 3: Build the CLI command
    cli_command = build_cli_command(exec_function, parameters)

    # Step 4: Run the segmentation
    run_segmentation(cli_command)

    # # Step 5: Pack outputs into a Docker image
    # output_dir = next(output["path"] for output in outputs)
    # pack_outputs_to_docker(output_dir)

if __name__ == "__main__":
    main()