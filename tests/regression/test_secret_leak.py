"""Defense in depth: even if a secret somehow carries a default, no generator may write it out.

The schema now rejects a secret default (tests/test_config/test_secret_validation.py), but
`generate` does not validate, so this pins the generators themselves.
"""

import subprocess
from importlib.resources import as_file

from tests.algorithm_discovery import config_resource

SENTINEL = "LEAKME123"
INTERFACES = ["gradio", "streamlit", "jupyter", "cellprofiler_plugin"]


def test_secret_default_never_leaks(tmp_path) -> None:
    with as_file(config_resource("cellsam_inference")) as config_path:
        text = config_path.read_text()
    anchor = "  label: DeepCell Access Token\n"
    assert anchor in text
    config = tmp_path / "config.yaml"
    config.write_text(text.replace(anchor, f"{anchor}  default: {SENTINEL}\n", 1))

    for interface in INTERFACES:
        result = subprocess.run(
            ["bilayers_cli", "generate", str(config), "-i", interface],
            cwd=tmp_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert result.returncode == 0 and "Error" not in result.stdout, f"{interface}: {result.stdout}\n{result.stderr}"

    leaks = [p for p in (tmp_path / "dist").rglob("*") if p.is_file() and SENTINEL in p.read_text(errors="ignore")]
    assert not leaks, f"secret default leaked into: {leaks}"
