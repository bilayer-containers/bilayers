import sys
import argparse

from .parse import parse_config, safe_parse_config, load_config
from .generate import generate_all, generate_interface
from .cli_generator import generate_cli_command

try:
    import linkml.validator
except ImportError:
    linkml = None


def cli() -> None:  # noqa: C901
    """CLI entry point for bilayers_cli"""

    # Creating an ArgumentParser object with a brief description of the tool
    # This automatically adds support for -h/--help
    parser = argparse.ArgumentParser(description="Bilayers CLI tool that parses a Bilayers YAML config file and generates an executable CLI command.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # parse subcommand
    parse_parser = subparsers.add_parser("parse", help="Parse a Bilayers YAML config file.")
    parse_parser.add_argument("config", help="Path to the YAML config file.")

    # generate subcommand
    generate_parser = subparsers.add_parser("generate", help="Generate outputs from a Bilayers YAML config file.")
    generate_parser.add_argument("config", help="Path to the YAML config file.")
    generate_parser.add_argument(
        "-i",
        "--interface",
        help='Name of specific interface to generate (e.g. gradio, jupyter) or "all" for every interface. If not provided, "all" is assumed by default.',
    )
    generate_parser.add_argument("--cli", action="store_true", help="Generate CLI command string instead of generating full interface")

    if linkml:
        validate_parser = subparsers.add_parser("validate", help="Validate a Bilayers YAML config file.")
        validate_parser.add_argument("config", help="Path to the YAML config file.")

    # Using action="version" automatically prints the version string and exits
    parser.add_argument("-v", "--version", action="version", version="bilayers_cli 0.1.0", help="Show the version number and exit.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Retrieve the config file path from the parsed arguments
    config_path = args.config

    if args.command == "parse":
        try:
            inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image = safe_parse_config(args.config)

            print(f"Inputs: {inputs}")
            print(f"Outputs: {outputs}")
            print(f"Parameters: {parameters}")
            print(f"Display Only: {display_only}")
            print(f"Exec Function: {exec_function}")
            print(f"Folder Name: {algorithm_folder_name}")
            print(f"Citations: {citations}")
            print(f"Docker Image: {docker_image['org']}/{docker_image['name']} ({docker_image['tag']}) - {docker_image['platform']}")
        except Exception as e:
            print(f"Error parsing config: {e}")
            sys.exit(1)

    elif args.command == "generate":
        if args.cli:
            try:
                parsed_config = parse_config(config_path)
                cli_command: str = str(generate_cli_command(parsed_config, return_as_string=True))
                print("Generated CLI Command:")
                print(cli_command)
            except Exception as e:
                print(f"Error: generating CLI command: {e}")
                sys.exit(1)
        elif args.interface and args.interface != "all":
            try:
                generate_interface(args.interface, config_path)
                print("Finished generating interface: {args.interface}")
            except Exception as e:
                print(f"Error: generating interface {args.interface}: {e}")
                sys.exit(1)
        else:
            try:
                generate_all(config_path)
                print("Finished generating all interfaces")
            except Exception as e:
                print(f"Error: generating interfaces: {e}")
                sys.exit(1)

    elif linkml and args.command == "validate":
        from . import schema

        config_yaml = load_config(config_path)
        report = linkml.validator.validate(config_yaml, schema)

        if not report.results:
            print("No issues found")
        else:
            for result in report.results:
                print(f"[{result.severity.value}] {result.message}")
