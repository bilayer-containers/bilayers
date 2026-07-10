"""Integration: every shipped algorithm config validates against the schema.

Where test_validate_configs.py exercises hand-written dummy configs, this test
runs the *real* configs (discovered from the installed bilayers_algorithms
package) through `bilayers_cli validate`. Config <-> schema conformance is an
integration concern (it needs both repos), so it lives here in bilayers rather
than in the algorithms repo.
"""

import subprocess
from importlib.resources import as_file

import pytest

from tests.algorithm_discovery import ALGORITHMS, config_resource


def test_algorithm_configs_discovered() -> None:
    # Guards against the parametrized test silently collecting nothing.
    assert ALGORITHMS, "no algorithm configs discovered in bilayers_algorithms"


@pytest.mark.parametrize("name", ALGORITHMS)
def test_config_validates_against_schema(name: str) -> None:
    with as_file(config_resource(name)) as path:
        result = subprocess.run(
            ["bilayers_cli", "validate", str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    output = result.stdout.strip()
    assert output == "No issues found", f"{name}/config.yaml failed schema validation:\n{output}\n{result.stderr}"
