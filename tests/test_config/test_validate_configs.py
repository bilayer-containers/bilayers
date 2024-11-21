import pytest
import subprocess
import os
import subprocess

@pytest.fixture
def schema_path():
    """Fixture for the path to the validation schema."""
    return "tests/test_config/validate_schema.yaml"

@pytest.mark.parametrize("config_path, expected_error", [
    # ("tests/test_algorithm/valid_config.yaml", "No issues found"),
    ("tests/test_algorithm/parameter_invalid_config.yaml", "[ERROR] [tests/test_algorithm/parameter_config.yaml/0] 'append_value' is a required property in /parameters/2")
])
def test_specific_validation_errors(schema_path, config_path, expected_error):
    """
    Test that the validation throws the exact expected error for multiple configurations.
    Test cases would bark at LinkML Validation level if any extra flags are passed.
    But they wouldn't bark if types are different and still you have added some special flag from different type
    """
    result = subprocess.run(
        ["linkml", "validate", "--schema", schema_path, "--target-class", "Container", config_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Assert the validation fails
    assert result.returncode == 0, f"Validation passed for {config_path}"

    # Check the exact error in the output
    error_lines = result.stdout.strip().split("\n")  # Split stdout into individual lines
    assert len(error_lines) == 1, f"Unexpected number of errors: {error_lines}"
    assert expected_error in error_lines, f"Unexpected error: {error_lines}"