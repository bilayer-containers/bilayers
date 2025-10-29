"""Module introspection utilities for discovering and scaffolding callable objects."""

from .discovery import discover_callables, FunctionMetadata
from .resolver import PackageResolver, PackageSource
from .containerize import (
    build_introspection_image,
    discover_in_container,
    build_algorithm_image,
    generate_introspection_dockerfile,
    generate_algorithm_dockerfile,
)

__all__ = [
    "discover_callables",
    "FunctionMetadata",
    "PackageResolver",
    "PackageSource",
    "build_introspection_image",
    "discover_in_container",
    "build_algorithm_image",
    "generate_introspection_dockerfile",
    "generate_algorithm_dockerfile",
]
