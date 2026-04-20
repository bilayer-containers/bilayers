"""
Tests for InterfaceLoader - capability checks and helpful install hints (#158).
"""

from pathlib import Path

import pytest

from bilayers.interface_loader import InterfaceLoader, MissingInterfaceDependencyError


def test_load_module_missing_optional_dependency(tmp_path: Path) -> None:
    """MissingInterfaceDependencyError is raised (not bare ImportError) when an
    interface's optional dep is absent, and the message contains an install hint."""
    interfaces_dir = tmp_path / "interfaces"
    interface_dir = interfaces_dir / "gradio"
    interface_dir.mkdir(parents=True)
    (interface_dir / "generate.py").write_text(
        "import definitely_missing_dependency_for_bilayers_test\n\n\ndef generate(interface_input):\n    return interface_input\n"
    )

    loader = InterfaceLoader(interfaces_dir)

    with pytest.raises(MissingInterfaceDependencyError, match=r"pip install bilayers\[gradio\]"):
        loader.load_module("gradio")


def test_missing_interface_has_install_hint(tmp_path: Path) -> None:
    """FileNotFoundError for an unknown interface includes a pip install hint."""
    interfaces_dir = tmp_path / "interfaces"
    interfaces_dir.mkdir(parents=True)

    loader = InterfaceLoader(interfaces_dir)

    with pytest.raises(FileNotFoundError, match=r"Install with: pip install bilayers\[jupyter\]"):
        loader.get_generate_path("jupyter")
