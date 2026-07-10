"""Integration smoke test: generation succeeds for every shipped algorithm.

Runs the full parse -> generate pipeline for each real algorithm config and
asserts every interface produces its expected, non-empty output file. This is
the broad "smoke for all algorithms" companion to the deep, byte-exact golden
check in test_generate_regression.py (which covers one representative config).
"""

import subprocess
from importlib.resources import as_file

import pytest

from tests.algorithm_discovery import ALGORITHMS, config_resource

# interface -> filename glob expected under dist/<interface>/<algorithm>/
EXPECTED_OUTPUTS = {
    "gradio": "app.py",
    "jupyter": "generated_notebook.ipynb",
    "streamlit": "streamlit_app.py",
    "cellprofiler_plugin": "*.py",
}


@pytest.mark.parametrize("name", ALGORITHMS)
def test_generate_produces_outputs(name: str, tmp_path) -> None:
    with as_file(config_resource(name)) as config_path:
        result = subprocess.run(
            ["bilayers_cli", "generate", str(config_path)],
            cwd=tmp_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    assert result.returncode == 0, f"generate failed for {name}:\n{result.stdout}\n{result.stderr}"

    dist = tmp_path / "dist"
    for interface, pattern in EXPECTED_OUTPUTS.items():
        matches = list(dist.glob(f"{interface}/*/{pattern}"))
        assert matches, f"{name}: no {interface} output (expected dist/{interface}/*/{pattern})\n{result.stdout}"
        assert matches[0].stat().st_size > 0, f"{name}: {interface} output is empty ({matches[0]})"
