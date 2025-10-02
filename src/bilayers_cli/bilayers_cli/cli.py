import sys
import argparse
from bilayers.build.parse.parse import parse_config
from bilayers_cli.bilayers_cli.cli_generator import main

def cli() -> None:
    """CLI entry point for bilayers_cli"""

    # Creating an ArgumentParser object with a brief description of the tool
    # This automatically adds support for -h/--help
    parser = argparse.ArgumentParser(
        description="Bilayers CLI tool that parses a Bilayers YAML config file and generates an executable CLI command."
    )

    # Add a positional argument for the YAML configuration file
    # When the user provides this argument, it will be stored in args.config
    parser.add_argument(
        "config",
        help="Path to the Bilayers YAML config file."
    )

    # Add an option to show the version of the CLI tool
    # Using action="version" automatically prints the version string and exits
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="bilayers_cli 0.1.0",
        help="Show the version number and exit."
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Retrieve the config file path from the parsed arguments
    config_path = args.config

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
