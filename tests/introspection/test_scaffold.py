"""Tests for the scaffold module."""

import pytest
from bilayers.introspection.discovery import FunctionMetadata, ParameterInfo
from bilayers.introspection.scaffold import scaffold_spec, _map_type_to_widget


def test_map_type_to_widget_bool():
    """Test mapping boolean types."""
    input_type, widget = _map_type_to_widget("bool")
    assert input_type == "boolean"
    assert widget == "checkbox"


def test_map_type_to_widget_int():
    """Test mapping integer types."""
    input_type, widget = _map_type_to_widget("int")
    assert input_type == "integer"
    assert widget == "slider"


def test_map_type_to_widget_float():
    """Test mapping float types."""
    input_type, widget = _map_type_to_widget("float")
    assert input_type == "float"
    assert widget == "slider"


def test_map_type_to_widget_str():
    """Test mapping string types."""
    input_type, widget = _map_type_to_widget("str")
    assert input_type == "string"
    assert widget == "textbox"


def test_map_type_to_widget_ndarray():
    """Test mapping numpy array types."""
    input_type, widget = _map_type_to_widget("ndarray")
    assert input_type == "file"
    assert widget == "file_upload"


def test_scaffold_spec_simple_function():
    """Test scaffolding a simple function."""
    # Create metadata for a simple function
    params = [
        ParameterInfo(name="x", annotation="int", default=None),
        ParameterInfo(name="y", annotation="float", default="1.0"),
    ]

    metadata = FunctionMetadata(
        module="test_module",
        name="test_func",
        qualname="test_func",
        signature="(x: int, y: float = 1.0) -> str",
        parameters=params,
        return_annotation="str",
        docstring="A test function that does something.",
    )

    spec = scaffold_spec(metadata)

    # Check that spec contains expected sections
    assert "algorithm:" in spec
    assert "name: test_func" in spec
    assert "module: test_module" in spec
    assert "introspection:" in spec
    assert "parameters:" in spec
    assert "outputs:" in spec
    assert "execution:" in spec

    # Check parameter details
    assert "name: x" in spec
    assert "name: y" in spec
    assert "type: integer" in spec
    assert "type: float" in spec
    assert "default: 1.0" in spec


def test_scaffold_spec_with_file_inputs():
    """Test scaffolding a function with file inputs."""
    params = [
        ParameterInfo(name="image", annotation="ndarray", default=None),
        ParameterInfo(name="threshold", annotation="float", default="0.5"),
    ]

    metadata = FunctionMetadata(
        module="skimage.filters",
        name="threshold_otsu",
        qualname="threshold_otsu",
        signature="(image: ndarray, threshold: float = 0.5) -> ndarray",
        parameters=params,
        return_annotation="ndarray",
        docstring="Apply Otsu threshold.",
    )

    spec = scaffold_spec(metadata)

    # Should have inputs section for file parameters
    assert "inputs:" in spec
    assert "name: image" in spec

    # Should have parameters section for non-file parameters
    assert "parameters:" in spec
    assert "name: threshold" in spec


def test_scaffold_spec_with_source():
    """Test scaffolding with a package source."""
    params = [ParameterInfo(name="x", annotation="int", default=None)]

    metadata = FunctionMetadata(
        module="test_module",
        name="test_func",
        qualname="test_func",
        signature="(x: int) -> str",
        parameters=params,
        return_annotation="str",
    )

    source = "pypi:test-package==1.0.0"
    spec = scaffold_spec(metadata, source=source)

    # Check that source is included
    assert f"Source: {source}" in spec
    assert f"source: {source}" in spec


def test_scaffold_spec_execution_command():
    """Test that execution command is properly generated."""
    params = [ParameterInfo(name="x", annotation="int", default=None)]

    metadata = FunctionMetadata(
        module="my_module",
        name="my_func",
        qualname="my_func",
        signature="(x: int) -> str",
        parameters=params,
        return_annotation="str",
    )

    spec = scaffold_spec(metadata)

    # Check execution section
    assert "execution:" in spec
    assert "command: python" in spec
    assert "- -m" in spec
    assert "- bilayers.introspection.exec" in spec
    assert "- --module" in spec
    assert "- my_module" in spec
    assert "- --function" in spec
    assert "- my_func" in spec
    assert "- --args-file" in spec


def test_scaffold_spec_interfaces():
    """Test that interface hints are included."""
    params = []

    metadata = FunctionMetadata(
        module="test_module",
        name="test_func",
        qualname="test_func",
        signature="() -> str",
        parameters=params,
        return_annotation="str",
    )

    spec = scaffold_spec(metadata)

    assert "interfaces:" in spec
    assert "gradio:" in spec
    assert "jupyter:" in spec
    assert "enabled: true" in spec
