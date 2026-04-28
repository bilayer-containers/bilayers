import json
import shutil
import subprocess
from pathlib import Path


def normalize_notebook(path: Path):
    with open(path) as f:
        nb = json.load(f)

    for cell in nb.get("cells", []):
        cell.pop("id", None)

    return nb


def test_generate_regression():
    repo_root = Path(__file__).resolve().parents[2]

    config_path = repo_root / "algorithms" / "classical_segmentation" / "config.yaml"
    golden_dir = repo_root / "tests" / "fixtures" / "golden" / "classical_segmentation"
    generated_root = repo_root / "dist"

    if generated_root.exists():
        shutil.rmtree(generated_root)

    subprocess.run(
        [
            "bilayers_cli",
            "generate",
            str(config_path),
        ],
        check=True,
        cwd=repo_root,
    )

    expected_outputs = {
        "gradio": (golden_dir, generated_root / "gradio" / "classical_segmentation" / "app.py"),
        "jupyter": (golden_dir, generated_root / "jupyter" / "classical_segmentation" / "generated_notebook.ipynb"),
        "streamlit": (golden_dir, generated_root / "streamlit" / "classical_segmentation" / "streamlit_app.py"),
        "cellprofiler_plugin": (golden_dir, generated_root / "cellprofiler_plugin" / "classical_segmentation" / "runclassicalsegmentation.py"),
    }

    for interface_name, (golden_base_dir, generated_file) in expected_outputs.items():
        assert generated_file.exists(), f"Missing generated file for {interface_name}: {generated_file}"

        if generated_file.suffix == ".ipynb":
            golden_file = golden_base_dir / "generated_notebook.ipynb"
            assert normalize_notebook(golden_file) == normalize_notebook(generated_file)
        else:
            if interface_name == "gradio":
                golden_file = golden_base_dir / "app.py"
            elif interface_name == "streamlit":
                golden_file = golden_base_dir / "streamlit_app.py"
            else:
                golden_file = golden_base_dir / "runclassicalsegmentation.py"

            assert golden_file.read_text() == generated_file.read_text()
