from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from bilayers.interface_loader import InterfaceLoader, MissingInterfaceDependencyError


def test_list_interfaces_returns_registry_names() -> None:
    fake_module = SimpleNamespace(generate=MagicMock())

    with patch("bilayers_targets.available_ifaces", {"gradio": fake_module, "jupyter": fake_module}):
        loader = InterfaceLoader()

    assert loader.list_interfaces() == ["gradio", "jupyter"]


def test_missing_interface_has_install_hint() -> None:
    with patch("bilayers_targets.available_ifaces", {}):
        loader = InterfaceLoader()

    with pytest.raises(MissingInterfaceDependencyError, match=r"pip install bilayers\[gradio\]"):
        loader.load_module("gradio")


def test_load_module_success() -> None:
    fake_module = SimpleNamespace(generate=MagicMock())

    with patch("bilayers_targets.available_ifaces", {"gradio": fake_module}):
        loader = InterfaceLoader()

    assert loader.load_module("gradio") is fake_module


def test_load_module_without_generate_raises() -> None:
    fake_module = SimpleNamespace()

    with patch("bilayers_targets.available_ifaces", {"gradio": fake_module}):
        loader = InterfaceLoader()

    with pytest.raises(AttributeError, match="does not provide callable generate"):
        loader.load_module("gradio")


def test_load_module_with_non_callable_generate_raises() -> None:
    fake_module = SimpleNamespace(generate="not_callable")

    with patch("bilayers_targets.available_ifaces", {"gradio": fake_module}):
        loader = InterfaceLoader()

    with pytest.raises(AttributeError, match="does not provide callable generate"):
        loader.load_module("gradio")
