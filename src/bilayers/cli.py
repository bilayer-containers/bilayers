import sys
import argparse
from pathlib import Path

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

    # discover subcommand (discovers functions in Docker container)
    discover_parser = subparsers.add_parser(
        "discover", help="Discover functions in an isolated Docker container."
    )
    discover_parser.add_argument("module", help="Module name to introspect")
    discover_parser.add_argument("--source", required=True, help="Package source (local:/path, pypi:package==version, git:url@ref)")
    discover_parser.add_argument("--output", "-o", default="./.introspection/discovery.json", help="Output path for JSON results (default: ./.introspection/discovery.json)")
    discover_parser.add_argument("--filter", help="Regex pattern to filter function names")
    discover_parser.add_argument("--include-private", action="store_true", help="Include private functions")
    discover_parser.add_argument("--python-version", default="3.11", help="Python version (e.g., 3.9, 3.10, 3.11, 3.12)")
    discover_parser.add_argument("--image-name", default="bilayers-introspect", help="Docker image name")
    discover_parser.add_argument("--keep-image", action="store_true", help="Keep Docker image after discovery")

    # scaffold subcommand (generates complete algorithm folder)
    scaffold_parser = subparsers.add_parser("scaffold", help="Generate complete algorithm folder from discovery results.")
    scaffold_parser.add_argument("discovery_json", nargs="?", default="./.introspection/discovery.json", help="Path to discovery JSON output (default: ./.introspection/discovery.json)")
    scaffold_parser.add_argument("function_name", help="Function name to scaffold")
    scaffold_parser.add_argument("--source", required=True, help="Package source (local:/path, pypi:package==version, git:url@ref)")
    scaffold_parser.add_argument("--output", "-o", default="./algorithms", help="Output directory for algorithm folder (default: ./algorithms)")
    scaffold_parser.add_argument("--python-version", default="3.11", help="Python version for Dockerfile (default: 3.11)")

    # build-algorithm subcommand
    build_algorithm_parser = subparsers.add_parser("build-algorithm", help="Build Docker image for a discovered algorithm.")
    build_algorithm_parser.add_argument("algorithm_folder", nargs="?", help="Path to algorithm folder (default: inferred from function name)")
    build_algorithm_parser.add_argument("--image-name", required=True, help="Docker image name")
    build_algorithm_parser.add_argument("--tag", default="latest", help="Docker image tag")
    build_algorithm_parser.add_argument("--function-name", help="Function name (used to find algorithm in ./algorithms/{function_name}/ if algorithm_folder not provided)")

    if linkml:
        validate_parser = subparsers.add_parser("validate", help="Validate a Bilayers YAML config file.")
        validate_parser.add_argument("config", help="Path to the YAML config file.")

    # Using action="version" automatically prints the version string and exits
    parser.add_argument("-v", "--version", action="version", version="bilayers_cli 0.1.0", help="Show the version number and exit.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Retrieve the config file path from the parsed arguments (only for commands that need it)
    config_path = getattr(args, "config", None)

    if args.command == "parse":
        try:
            inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations = safe_parse_config(args.config)

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
                print(f"Finished generating interface: {args.interface}")
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

    elif args.command == "discover":
        from .introspection.containerize import build_introspection_image, discover_in_container
        from .introspection.resolver import PackageSource

        try:
            # Parse source
            source = PackageSource.from_string(args.source)

            # Ensure output directory exists
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Build introspection image
            print(f"Building introspection Docker image for {source.location} (Python {args.python_version})...")
            image_name = build_introspection_image(source, args.image_name, tag="introspect", python_version=args.python_version)
            print(f"Built image: {image_name}")

            # Run discovery in container
            print(f"Discovering functions in {args.module}...")
            results = discover_in_container(
                image_name,
                args.module,
                include_private=args.include_private,
                filter_pattern=args.filter,
                output_path=output_path,
            )

            # Print summary
            print(f"\nDiscovered {len(results)} functions:")
            for func in results:
                print(f"  - {func.name}{func.signature}")

            # Clean up image unless requested to keep
            if not args.keep_image:
                import subprocess

                print(f"\nCleaning up image {image_name}...")
                subprocess.run(["docker", "rmi", image_name], capture_output=True)

            if args.output:
                print(f"\nResults saved to {args.output}")

        except Exception as e:
            print(f"Error during Docker discovery: {e}")
            sys.exit(1)

    elif args.command == "scaffold":
        from .introspection.discovery import load_discovery_results
        from .introspection.scaffold import scaffold_algorithm_folder

        try:
            # Load discovery results
            discovery_path = Path(args.discovery_json)
            if not discovery_path.exists():
                print(f"Error: Discovery file not found: {args.discovery_json}")
                sys.exit(1)

            results = load_discovery_results(discovery_path)

            # Find the requested function
            target_func = None
            for func in results:
                if func.name == args.function_name:
                    target_func = func
                    break

            if not target_func:
                print(f"Function '{args.function_name}' not found in discovery results")
                print(f"Available functions: {', '.join(r.name for r in results)}")
                sys.exit(1)

            # Generate complete algorithm folder
            output_dir = Path(args.output)
            algo_folder = scaffold_algorithm_folder(
                target_func,
                args.source,
                output_dir,
                python_version=args.python_version
            )

            print(f"Generated algorithm folder for {args.function_name} at {algo_folder}")
            print(f"\nFolder structure:")
            print(f"  {algo_folder}/")
            print(f"    ├── config.yaml")
            print(f"    ├── Dockerfile")
            print(f"    ├── {args.function_name}.py")
            print(f"    ├── __main__.py")
            print(f"    └── __init__.py")

        except Exception as e:
            print(f"Error during scaffolding: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    elif args.command == "build-algorithm":
        import subprocess

        try:
            # Determine algorithm folder path
            if args.algorithm_folder:
                algo_folder = Path(args.algorithm_folder)
            elif args.function_name:
                algo_folder = Path(f"./algorithms/{args.function_name}")
            else:
                print("Error: Must provide either algorithm_folder or --function-name")
                sys.exit(1)

            if not algo_folder.exists():
                print(f"Error: Algorithm folder not found: {algo_folder}")
                sys.exit(1)

            # Check for Dockerfile
            dockerfile = algo_folder / "Dockerfile"
            if not dockerfile.exists():
                print(f"Error: Dockerfile not found in {algo_folder}")
                sys.exit(1)

            # Build base image using standard docker build
            base_image_name = f"{args.image_name}-base"
            full_base_image_name = f"{base_image_name}:{args.tag}"

            print(f"Building algorithm base image: {full_base_image_name}")
            print(f"Building from: {algo_folder}")

            subprocess.run(
                ["docker", "build", "-t", full_base_image_name, "."],
                cwd=algo_folder,
                check=True,
            )

            print(f"\nSuccessfully built algorithm base image: {full_base_image_name}")
            print(f"\nTo use with Bilayers, generate interfaces from config.yaml:")
            print(f"  bilayers_cli generate {algo_folder}/config.yaml")

        except subprocess.CalledProcessError as e:
            print(f"Error building Docker image")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
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
