from unittest.mock import MagicMock, patch

import pytest

from bilayers.interface_loader import InterfaceLoader, MissingInterfaceDependencyError


class FakeEntryPoint:
    def __init__(self, name, loaded_value=None, import_error_name=None):
        self.name = name
        self._loaded_value = loaded_value
        self._import_error_name = import_error_name

    def load(self):
        if self._import_error_name:
            raise ImportError(f"No module named {self._import_error_name}", name=self._import_error_name)
        return self._loaded_value


def _make_entry_point(name: str, loaded_value):
    return FakeEntryPoint(name=name, loaded_value=loaded_value)


def _make_broken_entry_point(name: str, missing_dependency: str):
    return FakeEntryPoint(name=name, import_error_name=missing_dependency)


def _mock_entry_points(*fake_eps):
    """Mock the modern entry_points().select(group=...) API."""
    discovered = MagicMock()
    discovered.select.return_value = list(fake_eps)
    return discovered


def test_list_interfaces_returns_entry_point_names() -> None:
    """list_interfaces() returns sorted names of all registered entry points."""
    fake_eps = [
        _make_entry_point("gradio", MagicMock()),
        _make_entry_point("jupyter", MagicMock()),
    ]

    with patch("bilayers.interface_loader.entry_points", return_value=_mock_entry_points(*fake_eps)):
        loader = InterfaceLoader()

    assert loader.list_interfaces() == ["gradio", "jupyter"]


def test_load_generate_missing_optional_dependency() -> None:
    """MissingInterfaceDependencyError is raised when an interface optional dependency is absent."""
    fake_ep = _make_broken_entry_point("gradio", "definitely_missing_dependency_for_bilayers_test")

    with patch("bilayers.interface_loader.entry_points", return_value=_mock_entry_points(fake_ep)):
        loader = InterfaceLoader()

    with pytest.raises(MissingInterfaceDependencyError) as exc_info:
        loader.load_generate("gradio")

    message = str(exc_info.value)
    assert "Interface 'gradio' could not be loaded" in message
    assert "definitely_missing_dependency_for_bilayers_test" in message
    assert "pip install bilayers[gradio]" in message


def test_missing_interface_has_install_hint() -> None:
    """FileNotFoundError for an unknown interface includes a pip install hint."""
    with patch("bilayers.interface_loader.entry_points", return_value=_mock_entry_points()):
        loader = InterfaceLoader()

    with pytest.raises(FileNotFoundError) as exc_info:
        loader.load_generate("missing_interface")

    assert "Interface 'missing_interface' not found" in str(exc_info.value)
    assert "pip install bilayers[missing_interface]" in str(exc_info.value)


def test_load_generate_success() -> None:
    """load_generate() returns the callable when entry point loads cleanly."""
    fake_generate = MagicMock()
    fake_ep = _make_entry_point("gradio", fake_generate)

    with patch("bilayers.interface_loader.entry_points", return_value=_mock_entry_points(fake_ep)):
        loader = InterfaceLoader()

    assert loader.load_generate("gradio") is fake_generate


def test_load_generate_non_callable_raises() -> None:
    """AttributeError is raised if the entry point does not resolve to a callable."""
    fake_ep = _make_entry_point("gradio", "not_a_callable")

    with patch("bilayers.interface_loader.entry_points", return_value=_mock_entry_points(fake_ep)):
        loader = InterfaceLoader()

    with pytest.raises(AttributeError) as exc_info:
        loader.load_generate("gradio")

    assert "does not resolve to a callable" in str(exc_info.value)


def test_entry_points_py39_fallback() -> None:
    """InterfaceLoader supports the Python 3.9 entry_points() dict-like fallback."""
    fake_generate = MagicMock()
    fake_ep = _make_entry_point("gradio", fake_generate)

    with patch(
        "bilayers.interface_loader.entry_points",
        return_value={"bilayers.interfaces": [fake_ep]},
    ):
        loader = InterfaceLoader()

    assert loader.list_interfaces() == ["gradio"]
    assert loader.load_generate("gradio") is fake_generate
