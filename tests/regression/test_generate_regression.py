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
    generated_dir = repo_root / "algorithms" / "classical_segmentation" / "generated_folders" / "classical_segmentation"

    if generated_dir.exists():
        shutil.rmtree(generated_dir)

    subprocess.run(
        [
            "bilayers_cli",
            "generate",
            str(config_path),
        ],
        check=True,
        cwd=repo_root,
    )

    golden_files = sorted(p.relative_to(golden_dir) for p in golden_dir.rglob("*") if p.is_file())
    generated_files = sorted(p.relative_to(generated_dir) for p in generated_dir.rglob("*") if p.is_file())

    assert golden_files == generated_files

    for rel_path in golden_files:
        golden_file = golden_dir / rel_path
        generated_file = generated_dir / rel_path

        if golden_file.suffix == ".ipynb":
            assert normalize_notebook(golden_file) == normalize_notebook(generated_file)
        else:
            assert golden_file.read_text() == generated_file.read_text()
