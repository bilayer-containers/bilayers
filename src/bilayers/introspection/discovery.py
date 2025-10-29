"""Discovery utilities for enumerating and inspecting callable objects in Python modules."""

import importlib
import inspect
import sys
from dataclasses import dataclass, asdict, field
from typing import Any, Callable, Optional, get_type_hints
from pathlib import Path


@dataclass
class ParameterInfo:
    """Metadata about a function parameter."""

    name: str
    annotation: str
    default: Optional[str] = None
    kind: str = "POSITIONAL_OR_KEYWORD"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class FunctionMetadata:
    """Metadata about a discovered callable function."""

    module: str
    name: str
    qualname: str
    signature: str
    parameters: list[ParameterInfo] = field(default_factory=list)
    return_annotation: str = "Any"
    docstring: Optional[str] = None
    source_file: Optional[str] = None
    line_number: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result["parameters"] = [p.to_dict() for p in self.parameters]
        return result


def _format_annotation(annotation: Any) -> str:
    """Format a type annotation as a string."""
    if annotation is inspect.Parameter.empty or annotation is inspect.Signature.empty:
        return "Any"

    # Handle string annotations
    if isinstance(annotation, str):
        return annotation

    # Handle types with __name__
    if hasattr(annotation, "__name__"):
        return annotation.__name__

    # Handle complex types (generics, etc.)
    return str(annotation).replace("typing.", "")


def _format_default(default: Any) -> Optional[str]:
    """Format a parameter default value as a string."""
    if default is inspect.Parameter.empty:
        return None

    # Handle common types
    if isinstance(default, (str, int, float, bool, type(None))):
        return repr(default)

    # For complex defaults, use repr but truncate if too long
    result = repr(default)
    if len(result) > 50:
        return f"{result[:47]}..."
    return result


def inspect_callable(func: Callable, module_name: str) -> Optional[FunctionMetadata]:
    """
    Inspect a callable and extract metadata.

    Args:
        func: The callable to inspect
        module_name: Name of the module containing the callable

    Returns:
        FunctionMetadata if inspection succeeds, None otherwise
    """
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        # Cannot inspect signature (e.g., built-ins, C extensions)
        return None

    # Extract parameter information
    parameters = []
    for param_name, param in sig.parameters.items():
        param_info = ParameterInfo(
            name=param_name,
            annotation=_format_annotation(param.annotation),
            default=_format_default(param.default),
            kind=str(param.kind).replace("_", " "),
        )
        parameters.append(param_info)

    # Get return annotation
    return_annotation = _format_annotation(sig.return_annotation)

    # Get source file and line number if available
    source_file = None
    line_number = None
    try:
        source_file = inspect.getsourcefile(func)
        _, line_number = inspect.getsourcelines(func)
    except (TypeError, OSError):
        pass

    # Get docstring
    docstring = inspect.getdoc(func)

    return FunctionMetadata(
        module=module_name,
        name=func.__name__,
        qualname=func.__qualname__,
        signature=str(sig),
        parameters=parameters,
        return_annotation=return_annotation,
        docstring=docstring,
        source_file=source_file,
        line_number=line_number,
    )


def discover_callables(
    module_name: str,
    include_private: bool = False,
    include_nested: bool = True,
    filter_pattern: Optional[str] = None,
) -> list[FunctionMetadata]:
    """
    Discover callable functions in a Python module.

    Args:
        module_name: Fully qualified module name to inspect (e.g., 'skimage.filters')
        include_private: Include functions starting with underscore
        include_nested: Include nested/inner functions
        filter_pattern: Optional regex pattern to filter function names

    Returns:
        List of FunctionMetadata for discovered callables

    Raises:
        ImportError: If the module cannot be imported
    """
    import re

    # Import the module
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(f"Failed to import module '{module_name}': {e}") from e

    discovered = []
    filter_re = re.compile(filter_pattern) if filter_pattern else None

    # Iterate over module attributes
    for attr_name in dir(module):
        # Skip private members if requested
        if not include_private and attr_name.startswith("_"):
            continue

        # Apply filter pattern if provided
        if filter_re and not filter_re.match(attr_name):
            continue

        try:
            attr = getattr(module, attr_name)
        except AttributeError:
            continue

        # Check if it's a callable function
        if not inspect.isfunction(attr) and not inspect.isbuiltin(attr):
            continue

        # Skip nested functions if requested
        if not include_nested and "." in getattr(attr, "__qualname__", ""):
            parent_qualname = attr.__qualname__.rsplit(".", 1)[0]
            if parent_qualname != attr_name:
                continue

        # Inspect the callable
        metadata = inspect_callable(attr, module_name)
        if metadata:
            discovered.append(metadata)

    return discovered


def save_discovery_results(results: list[FunctionMetadata], output_path: Path) -> None:
    """
    Save discovery results to a JSON file.

    Args:
        results: List of FunctionMetadata to save
        output_path: Path to output JSON file
    """
    import json

    data = [result.to_dict() for result in results]

    with output_path.open("w") as f:
        json.dump(data, f, indent=2)


def load_discovery_results(input_path: Path) -> list[FunctionMetadata]:
    """
    Load discovery results from a JSON file.

    Args:
        input_path: Path to input JSON file

    Returns:
        List of FunctionMetadata
    """
    import json

    with input_path.open("r") as f:
        data = json.load(f)

    results = []
    for item in data:
        # Reconstruct ParameterInfo objects
        parameters = [ParameterInfo(**p) for p in item.pop("parameters", [])]
        # Reconstruct FunctionMetadata
        metadata = FunctionMetadata(**item, parameters=parameters)
        results.append(metadata)

    return results
