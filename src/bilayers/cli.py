import sys
import argparse

from .parse import parse_config, main as parse_main
from .generate import main as generate_main
from .cli_generator import generate_cli_command


def cli() -> None:
    """CLI entry point for bilayers_cli"""

    # Creating an ArgumentParser object with a brief description of the tool
    # This automatically adds support for -h/--help
    parser = argparse.ArgumentParser(
        description="Bilayers CLI tool that parses a Bilayers YAML config file and generates an executable CLI command."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # parse subcommand
    parse_parser = subparsers.add_parser(
        "parse",
        help="Parse a Bilayers YAML config file."
    )
    parse_parser.add_argument("config", help="Path to the YAML config file.")

    # generate subcommand
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate outputs from a Bilayers YAML config file."
    )
    generate_parser.add_argument("config", help="Path to the YAML config file.")
    generate_parser.add_argument(
        "--cli",
        action="store_true",
        help="Generate CLI command string instead of generating full interface"
    )

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

    if args.command == "parse":
        try:
            inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations = parse_main(args.config)

            print(f"Inputs: {inputs}")
            print(f"Outputs: {outputs}")
            print(f"Parameters: {parameters}")
            print(f"Display Only: {display_only}")
            print(f"Exec Function: {exec_function}")
            print(f"Folder Name: {algorithm_folder_name}")
            print(f"Citations: {citations}")
        except Exception as e:
            print(f"Error parsing config: {e}")
            sys.exit(1)

    elif args.command == "generate":
        if args.cli:
            try:
                generate_main(config_path)
            except Exception as e:
                print(f"Error: generating interface: {e}")
                sys.exit(1)
        else:
            try:
                parsed_config = parse_config(config_path)
                cli_command: str = str(generate_cli_command(parsed_config, return_as_string=True))
                print("\nGenerated CLI Command:")
                print(cli_command)
            except Exception as e:
                print(f"Error: generating CLI command: {e}")
                sys.exit(1)

if __name__ == "__main__":
    cli()
