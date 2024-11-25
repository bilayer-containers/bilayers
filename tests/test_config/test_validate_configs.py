import pytest
import subprocess
import os
import subprocess

@pytest.fixture
def schema_path():
    """Fixture for the path to the validation schema."""
    return "tests/test_config/validate_schema.yaml"

@pytest.fixture
def config_files():
    """Fixture providing paths to multiple configuration files and expected errors."""
    return [
        ("tests/test_algorithm/empty_config.yaml", ["No issues found"]),  # Empty config, no errors

        (
            "tests/test_algorithm/parameter_invalid_config.yaml",
            [
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'append_value' is a required property in /parameters/2",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] Additional properties are not allowed ('extra_random_flag' was unexpected) in /parameters/8",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'folder_name' is a required property in /parameters/14",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'file_count' is a required property in /parameters/14",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'random' is not one of ['single', 'multiple'] in /parameters/15/file_count",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'multiselect' is a required property in /parameters/22",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'append_value' is a required property in /parameters/30",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] Additional properties are not allowed ('cli_order', 'cli_tag' were unexpected) in /display_only/0",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] Additional properties are not allowed ('cli_tag' was unexpected) in /results/0",
            ],
        ),

        (
            "tests/test_algorithm/valid_config.yaml", ["No issues found"]
        ),
    ]

@pytest.mark.parametrize(
    "config_path, expected_error",
    [
        (
            "tests/test_algorithm/empty_config.yaml",
            ["No issues found"],
        ),
        (
            "tests/test_algorithm/parameter_invalid_config.yaml",
            [
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'append_value' is a required property in /parameters/2",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] Additional properties are not allowed ('extra_random_flag' was unexpected) in /parameters/8",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'folder_name' is a required property in /parameters/14",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'file_count' is a required property in /parameters/14",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'random' is not one of ['single', 'multiple'] in /parameters/15/file_count",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'multiselect' is a required property in /parameters/22",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] 'append_value' is a required property in /parameters/30",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] Additional properties are not allowed ('cli_order', 'cli_tag' were unexpected) in /display_only/0",
                "[ERROR] [tests/test_algorithm/parameter_invalid_config.yaml/0] Additional properties are not allowed ('cli_tag' was unexpected) in /results/0",
            ],
        ),
        (
            "tests/test_algorithm/valid_config.yaml",
            ["No issues found"],
        ),
    ],
)
def test_specific_validation_errors(schema_path, config_path, expected_error): 
    """
    Test that the validation throws the exact expected error for multiple configurations.
    Test cases would bark at LinkML Validation level if any extra flags are passed.
    But they wouldn't bark if types are different and still you have added some special flag from different type
    """
    # for config_path, expected_errors in config_files:
    result = subprocess.run(
        ["linkml", "validate", "--schema", schema_path, "--target-class", "Container", config_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Process the results
    assert expected_error == result.stdout.strip().split("\n")