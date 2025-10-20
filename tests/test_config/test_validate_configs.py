import pytest
import subprocess


@pytest.mark.parametrize(
    "config_path, expected_error",
    [
        (
            "tests/test_algorithm/empty_config.yaml",
            ["[ERROR] None is not of type 'object' in /"],
        ),
        (
            "tests/test_algorithm/incorrect_validation_config.yaml",
            [
                "[ERROR] 'append_value' is a required property in /parameters/2",
                "[ERROR] Additional properties are not allowed ('folder_name' was unexpected) in /parameters/3",
                "[ERROR] 'optional' is a required property in /parameters/4",
                "[ERROR] 'optional' is a required property in /parameters/5",
                "[ERROR] Additional properties are not allowed ('extra_random_flag' was unexpected) in /parameters/8",
                "[ERROR] Additional properties are not allowed ('file_count', 'folder_name' were unexpected) in /parameters/12",
                "[ERROR] 'files' is not one of ['integer', 'float', 'boolean', 'checkbox', 'dropdown', 'radio', 'textbox', 'image', 'measurement', 'array', 'file', 'executable'] in /parameters/12/type",
                "[ERROR] Additional properties are not allowed ('file_count', 'folder_name' were unexpected) in /parameters/13",
                "[ERROR] 'files' is not one of ['integer', 'float', 'boolean', 'checkbox', 'dropdown', 'radio', 'textbox', 'image', 'measurement', 'array', 'file', 'executable'] in /parameters/13/type",
                "[ERROR] 'files' is not one of ['integer', 'float', 'boolean', 'checkbox', 'dropdown', 'radio', 'textbox', 'image', 'measurement', 'array', 'file', 'executable'] in /parameters/14/type",
                "[ERROR] Additional properties are not allowed ('file_count', 'folder_name' were unexpected) in /parameters/15",
                "[ERROR] 'files' is not one of ['integer', 'float', 'boolean', 'checkbox', 'dropdown', 'radio', 'textbox', 'image', 'measurement', 'array', 'file', 'executable'] in /parameters/15/type",
                "[ERROR] 'multiselect' is a required property in /parameters/22",
                "[ERROR] Additional properties are not allowed ('file_count', 'folder_name' were unexpected) in /parameters/30",
                "[ERROR] 'append_value' is a required property in /parameters/30",
                "[ERROR] Additional properties are not allowed ('cli_order', 'cli_tag' were unexpected) in /display_only/0",
                "[ERROR] 'optional' is a required property in /display_only/0",
                "[ERROR] 'inputs' is a required property in /",
                "[ERROR] 'outputs' is a required property in /",
            ],
        ),
        (
            "tests/test_algorithm/correct_validation_config.yaml",
            ["No issues found"],
        ),
    ],
)
def test_specific_validation_errors(config_path: str, expected_error: list[str]) -> None:
    """
    Test that the validation throws the exact expected error for multiple configurations.
    Test cases would bark at LinkML Validation level if any extra flags are passed.
    But they wouldn't bark if types are different and still you have added some special flag from different type
    Args:
        config_path (str): The path to the configuration file to be validated.
        expected_error (list[str]): The expected validation error messages.
    """
    # for config_path, expected_errors in config_files:
    result: subprocess.CompletedProcess[str] = subprocess.run(
        ["bilayers_cli", "validate", config_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    # Process the results
    actual_output: list[str] = result.stdout.strip().split("\n")
    assert expected_error == actual_output, f"Expected: {expected_error}, Got: {actual_output}"
