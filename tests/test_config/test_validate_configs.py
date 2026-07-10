"""Validation behaviour on hand-crafted dummy configs.

These pin the *behaviour* of `bilayers_cli validate` - a valid config passes, a
broken one is rejected and reports the expected kinds of violations. We assert
on stable signals (presence of specific error kinds) rather than the exact,
full error list with /parameters/N indices, so the test survives schema
reordering and linkml message rewording. Validation of the real algorithm
configs lives in test_algorithm_configs.py.
"""

import subprocess

import pytest

CONFIG_DIR = "tests/test_algorithm"


def run_validate(config_path: str) -> str:
    result = subprocess.run(
        ["bilayers_cli", "validate", config_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def test_correct_config_has_no_issues() -> None:
    assert run_validate(f"{CONFIG_DIR}/correct_validation_config.yaml") == "No issues found"


def test_empty_config_is_rejected() -> None:
    output = run_validate(f"{CONFIG_DIR}/empty_config.yaml")
    assert output != "No issues found"
    assert "[ERROR]" in output


# Position-independent signals of the violations seeded into
# incorrect_validation_config.yaml - the *kinds* of errors, without pinning exact
# messages, indices, or the complete error set.
EXPECTED_ERROR_SIGNALS = [
    "'append_value' is a required property",  # checkbox rule
    "Additional properties are not allowed",  # unexpected flags
    "'optional' is a required property",  # missing required slot
    "is not one of",  # bad type enum value
    "'inputs' is a required property",  # missing top-level section
    "'outputs' is a required property",  # missing top-level section
]


@pytest.fixture(scope="module")
def incorrect_output() -> str:
    return run_validate(f"{CONFIG_DIR}/incorrect_validation_config.yaml")


def test_incorrect_config_is_rejected(incorrect_output: str) -> None:
    assert incorrect_output != "No issues found"
    assert "[ERROR]" in incorrect_output


@pytest.mark.parametrize("signal", EXPECTED_ERROR_SIGNALS)
def test_incorrect_config_reports_error_kind(incorrect_output: str, signal: str) -> None:
    assert signal in incorrect_output, f"expected a '{signal}' error; full output:\n{incorrect_output}"
