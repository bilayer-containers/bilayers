import bilayers
from bilayers.parse import parse_config
from bilayers.cli_generator import generate_cli_command


def test_main():
    # Use a real configuration file path from your project.
    config_path = bilayers.project_path() / "algorithms/classical_segmentation/config.yaml"

    # Parse the configuration file.
    config = parse_config(config_path)

    # Generate the CLI command (using return_as_string to get a single string output).
    cli_command = generate_cli_command(config, return_as_string=True)

    # Output the result.
    print("Generated CLI Command:")
    print(cli_command)


if __name__ == "__main__":
    test_main()
