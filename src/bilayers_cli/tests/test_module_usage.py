from src.bilayers.build.parse.parse import parse_config
from bilayers_cli.cli_generator import main

# Test if parsing config works
config_data = parse_config("../../bilayers/algorithms/instanseg_inference/config.yaml")
print("Parsed Config:", config_data)

# Test CLI command generation
cli_command = main(config_data, return_as_string=True)
print("Generated CLI Command:", cli_command)
