import pytest
from bilayers_cli.cli_generator import generate_cli_command

@pytest.fixture
def sample_config():
    """Sample YAML configuration converted to a dictionary for testing."""
    return {
        "exec_function": {
            "cli_command": "run_algorithm",
            "hidden_args": {
                "debug": {
                    "cli_tag": "--debug",
                    "value": "True",
                    "cli_order": 2,
                    "append_value": True
                },
                "log": {
                    "cli_tag": "--log",
                    "value": "/var/log/output.log",
                    "cli_order": 3
                }
            }
        },
        "inputs": {
            "input_file": {
                "name": "input_file",
                "type": "file",
                "cli_tag": "--input",
                "cli_order": 1,
                "default": "input.txt"
            }
        },
        "parameters": {
            "threshold": {
                "name": "threshold",
                "type": "integer",
                "cli_tag": "--threshold",
                "cli_order": -1,
                "default": 5
            },
            "verbose": {
                "name": "verbose",
                "type": "checkbox",
                "cli_tag": "--verbose",
                "cli_order": -2,
                "default": True,
                "append_value": False
            }
        }
    }

def test_generate_cli_command(sample_config):
    """Test CLI command generation with valid configuration."""
    cli_command = generate_cli_command(sample_config)

    # Expected order:
    # 1. `run_algorithm`
    # 2. `--input input.txt` (1)
    # 3. `--debug True` (2)
    # 4. `--log /var/log/output.log` (3)
    # 5. `--threshold 5` (-1)
    # 6. `--verbose` (-2) 
    expected_command = [
        "run_algorithm", "--input input.txt",
        "--debug True", "--log /var/log/output.log",
        "--verbose", "--threshold 5", 
    ]
    
    assert cli_command == expected_command

def test_hidden_arguments(sample_config):
    """Ensure hidden arguments are always included in the CLI output."""
    cli_command = generate_cli_command(sample_config)
    assert "--debug True" in cli_command
    assert "--log /var/log/output.log" in cli_command

def test_checkbox_without_append_value():
    """Test checkbox parameter without append_value should only include tag if True."""
    config = {
        "exec_function": {"cli_command": "run_algorithm"},
        "parameters": {
            "verbose": {
                "name": "verbose",
                "type": "checkbox",
                "cli_tag": "--verbose",
                "cli_order": 1,
                "default": True,
                "append_value": False
            }
        }
    }
    cli_command = generate_cli_command(config)
    assert cli_command == ["run_algorithm", "--verbose"]

def test_checkbox_with_append_value():
    """Test checkbox parameter with append_value should include tag and value."""
    config = {
        "exec_function": {"cli_command": "run_algorithm"},
        "parameters": {
            "verbose": {
                "name": "verbose",
                "type": "checkbox",
                "cli_tag": "--verbose",
                "cli_order": 1,
                "default": True,
                "append_value": True
            }
        }
    }
    cli_command = generate_cli_command(config)
    assert cli_command == ["run_algorithm", "--verbose True"]

def test_file_input():
    """Test input file handling correctly uses folder_name if provided."""
    config = {
        "exec_function": {"cli_command": "run_algorithm"},
        "inputs": {
            "input_file": {
                "name": "input_file",
                "type": "file",
                "cli_tag": "--input",
                "cli_order": 1,
                "default": "input.txt",
                "folder_name": "/tmp"
            }
        }
    }
    cli_command = generate_cli_command(config)
    assert cli_command == ["run_algorithm", "--input /tmp"]

def test_missing_required_argument():
    """Test required argument raises ValueError if missing."""
    config = {
        "exec_function": {"cli_command": "run_algorithm"},
        "parameters": {
            "threshold": {
                "name": "threshold",
                "type": "integer",
                "cli_tag": "--threshold",
                "cli_order": 1,
                "optional": False
            }
        }
    }
    with pytest.raises(ValueError, match="Error: 'threshold' is a required argument and must have a value!"):
        generate_cli_command(config)

def test_order_of_arguments():
    """Ensure arguments appear in the correct order based on cli_order."""
    config = {
        "exec_function": {"cli_command": "run_algorithm"},
        "parameters": {
            "first": {"cli_tag": "--first", "cli_order": 1, "default": "1"},
            "second": {"cli_tag": "--second", "cli_order": -1, "default": "2"},
            "third": {"cli_tag": "--third", "cli_order": 3, "default": "3"},
        }
    }
    cli_command = generate_cli_command(config)
    
    # Order should be: `run_algorithm` → `--first 1` (1) → `--third 3` (3) → `--second 2` (-1)
    assert cli_command == ["run_algorithm", "--first 1", "--third 3", "--second 2"]