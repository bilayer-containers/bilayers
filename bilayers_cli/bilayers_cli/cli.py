import sys
from bilayers_cli.parse import parse_config
from bilayers_cli.cli_generator import main

def cli() -> None:
    """CLI entry point for bilayers_cli"""
    if len(sys.argv) < 2:
        print("\nError: Please provide a Bilayers YAML config file.\n")
        print("Usage:")
        print("  bilayers_cli path/to/config.yaml\n")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        parsed_config = parse_config(config_path)  # Parse YAML file
        cli_command: str = str(main(parsed_config, return_as_string=True))  # CLI output in string format
        print("\nGenerated CLI Command:")
        print(cli_command)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    cli()
