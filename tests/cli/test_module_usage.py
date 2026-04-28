from pathlib import Path
from bilayers.parse import parse_config
from bilayers.cli_generator import generate_cli_command

# Test if parsing config works
config_data = parse_config(Path(__file__).resolve().parents[1] / "fixtures" / "classical_segmentation" / "config.yaml")
print("Parsed Config:", config_data)

# Test CLI command generation
cli_command = generate_cli_command(config_data, return_as_string=True)
print("Generated CLI Command:", cli_command)
