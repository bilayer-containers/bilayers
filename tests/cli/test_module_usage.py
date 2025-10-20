import bilayers
from bilayers.parse import parse_config
from bilayers.cli_generator import generate_cli_command

# Test if parsing config works
config_data = parse_config(bilayers.project_path() / "algorithms/instanseg_inference/config.yaml")
print("Parsed Config:", config_data)

# Test CLI command generation
cli_command = generate_cli_command(config_data, return_as_string=True)
print("Generated CLI Command:", cli_command)
