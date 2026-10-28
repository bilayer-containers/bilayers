"""Integration: `bilayers_cli validate` enforces that a secret parameter has no default.

Uses the real cellsam_inference config (the shipped algorithm with a secret) and
changes one parameter at a time, so a regression in the schema rules or in the
config shows up here. The rules are two: a secret must not have a default, and
every other type must have one.
"""

import subprocess
from importlib.resources import as_file

import pytest
import yaml

from tests.algorithm_discovery import config_resource

SECRET_NAME = "deepcell_access_token"


def cellsam_config() -> dict:
    with as_file(config_resource("cellsam_inference")) as path:
        return yaml.safe_load(path.read_text())


def parameter(config: dict, name: str) -> dict:
    return next(p for p in config["parameters"] if p["name"] == name)


def validate(tmp_path, config: dict) -> str:
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config, sort_keys=False))
    result = subprocess.run(["bilayers_cli", "validate", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()


def with_extra_parameter(config: dict, **overrides) -> dict:
    # Clone the secret's fields, then override name/type/default, so every required field is present
    extra = {k: v for k, v in parameter(config, SECRET_NAME).items() if k != "default"}
    extra.update(name="plain", **overrides)
    config["parameters"].append(extra)
    return config


def test_shipped_secret_has_no_default_and_validates(tmp_path) -> None:
    config = cellsam_config()
    assert "default" not in parameter(config, SECRET_NAME)
    assert validate(tmp_path, config) == "No issues found"


@pytest.mark.parametrize("value", ["abc", ""])
def test_secret_with_default_fails_validation(tmp_path, value) -> None:
    # "" still counts: the rule is about the key being present, not its value
    config = cellsam_config()
    parameter(config, SECRET_NAME)["default"] = value
    out = validate(tmp_path, config)
    assert out != "No issues found" and "[ERROR]" in out and "/parameters/" in out


def test_secret_without_allowed_suffix_fails_validation(tmp_path) -> None:
    config = cellsam_config()
    parameter(config, SECRET_NAME)["name"] = "path"
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config, sort_keys=False))
    result = subprocess.run(["bilayers_cli", "validate", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode != 0 and "env var 'PATH'" in result.stderr


def test_non_secret_without_default_validates(tmp_path) -> None:
    config = cellsam_config()
    del parameter(config, "model_name")["default"]
    assert validate(tmp_path, config) == "No issues found"


@pytest.mark.parametrize("param_type", ["integer", "float", "boolean", "textbox"])
def test_added_non_secret_without_default_validates(tmp_path, param_type) -> None:
    config = with_extra_parameter(cellsam_config(), type=param_type)
    assert validate(tmp_path, config) == "No issues found"


@pytest.mark.parametrize("param_type, default", [("integer", 1), ("float", 0.5), ("boolean", True), ("textbox", "x")])
def test_added_non_secret_with_default_validates(tmp_path, param_type, default) -> None:
    config = with_extra_parameter(cellsam_config(), type=param_type, default=default)
    assert validate(tmp_path, config) == "No issues found"
