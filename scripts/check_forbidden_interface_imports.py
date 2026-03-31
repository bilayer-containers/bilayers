#!/usr/bin/env python
import ast
import sys
from pathlib import Path

FORBIDDEN_MODULES = {
    "bilayers.parse",
    "bilayers.generate",
}

FORBIDDEN_BILAYERS_SYMBOLS = {
    "project_path",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_FILES = list((REPO_ROOT / "interfaces").glob("*/generate.py"))


def check_file(path: Path) -> list[str]:
    errors = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in FORBIDDEN_MODULES:
                    errors.append(
                        f"{path}:{node.lineno} forbidden import: import {alias.name}"
                    )

        elif isinstance(node, ast.ImportFrom):
            if node.module in FORBIDDEN_MODULES:
                errors.append(
                    f"{path}:{node.lineno} forbidden import: from {node.module} import ..."
                )

            if node.module == "bilayers":
                for alias in node.names:
                    if alias.name in FORBIDDEN_BILAYERS_SYMBOLS:
                        errors.append(
                            f"{path}:{node.lineno} forbidden import: from bilayers import {alias.name}"
                        )

    return errors


def main() -> int:
    all_errors = []
    for path in TARGET_FILES:
        all_errors.extend(check_file(path))

    if all_errors:
        print("Forbidden imports found:")
        for error in all_errors:
            print(error)
        return 1

    print("No forbidden imports found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
