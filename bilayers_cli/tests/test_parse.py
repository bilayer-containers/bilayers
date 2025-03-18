import pytest
import yaml
from bilayers_cli.parse import parse_config

@pytest.fixture
def sample_yaml(tmp_path):
    """Creates a sample Bilayers YAML config file for testing."""
    yaml_content = {
        "exec_function": {
            "cli_command": "run_algorithm",
            "hidden_args": []
        },
        "inputs": [
            {"name": "input_image", "type": "file", "cli_tag": "--image", "default": "input_images"}
        ],
        "parameters": [
            {"name": "threshold", "type": "integer", "cli_tag": "--threshold", "default": 128}
        ]
    }
    yaml_path = tmp_path / "config.yaml"
    with open(yaml_path, "w") as file:
        yaml.dump(yaml_content, file)

    return yaml_path

def test_parse_yaml(sample_yaml):
    """Test if parse_config correctly loads YAML content into a structured dictionary."""
    config = parse_config(str(sample_yaml))
    
    assert config["exec_function"]["cli_command"] == "run_algorithm"
    assert "input_image" in config["inputs"]
    assert config["inputs"]["input_image"]["cli_tag"] == "--image"
    assert config["parameters"]["threshold"]["cli_tag"] == "--threshold"
    assert config["parameters"]["threshold"]["default"] == 128