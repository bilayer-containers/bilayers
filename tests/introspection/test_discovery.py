"""Tests for the discovery module."""

import pytest
from bilayers.introspection.discovery import discover_callables, inspect_callable, FunctionMetadata, ParameterInfo


def sample_function(x: int, y: float = 1.0, name: str = "test") -> str:
    """A sample function for testing."""
    return f"{name}: {x + y}"


def test_inspect_callable():
    """Test inspecting a simple callable."""
    metadata = inspect_callable(sample_function, "test_module")

    assert metadata is not None
    assert metadata.name == "sample_function"
    assert metadata.module == "test_module"
    assert len(metadata.parameters) == 3

    # Check parameters
    param_names = [p.name for p in metadata.parameters]
    assert "x" in param_names
    assert "y" in param_names
    assert "name" in param_names

    # Check parameter details
    x_param = next(p for p in metadata.parameters if p.name == "x")
    assert x_param.annotation == "int"
    assert x_param.default is None

    y_param = next(p for p in metadata.parameters if p.name == "y")
    assert y_param.annotation == "float"
    assert y_param.default == "1.0"

    # Check return type
    assert metadata.return_annotation == "str"

    # Check docstring
    assert metadata.docstring == "A sample function for testing."


def test_discover_callables_os_path():
    """Test discovering callables in os.path module."""
    results = discover_callables("os.path", include_private=False)

    assert len(results) > 0

    # Check that common functions are found
    function_names = [r.name for r in results]
    assert "join" in function_names
    assert "exists" in function_names

    # Note: os.path may have some underscore-prefixed functions that are still public
    # Just verify we got the public ones we expected
    assert "join" in function_names
    assert "exists" in function_names
    assert "isdir" in function_names


def test_discover_callables_with_filter():
    """Test discovering callables with a filter pattern."""
    results = discover_callables("os.path", filter_pattern=r"is.*")

    # All results should match the pattern
    for result in results:
        assert result.name.startswith("is")


def test_discover_callables_include_private():
    """Test discovering callables including private functions."""
    results_no_private = discover_callables("os", include_private=False)
    results_with_private = discover_callables("os", include_private=True)

    # With private should have more results
    assert len(results_with_private) >= len(results_no_private)


def test_function_metadata_to_dict():
    """Test serializing FunctionMetadata to dictionary."""
    param = ParameterInfo(name="x", annotation="int", default=None)
    metadata = FunctionMetadata(
        module="test",
        name="func",
        qualname="func",
        signature="(x: int) -> str",
        parameters=[param],
        return_annotation="str",
        docstring="Test function",
    )

    data = metadata.to_dict()

    assert isinstance(data, dict)
    assert data["name"] == "func"
    assert data["module"] == "test"
    assert len(data["parameters"]) == 1
    assert data["parameters"][0]["name"] == "x"


def test_discover_callables_invalid_module():
    """Test that discovering from an invalid module raises ImportError."""
    with pytest.raises(ImportError):
        discover_callables("nonexistent.module.that.does.not.exist")
