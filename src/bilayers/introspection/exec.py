"""Execution shim for running introspected functions at runtime."""

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any


def load_args_from_file(args_file: Path) -> dict[str, Any]:
    """Load function arguments from a JSON file."""
    with args_file.open("r") as f:
        return json.load(f)


def resolve_file_paths(args: dict[str, Any]) -> dict[str, Any]:
    """
    Resolve file path strings to actual paths or loaded objects.

    This handles cases where arguments are file paths that need to be
    read or processed before passing to the function.
    """
    resolved = {}

    for key, value in args.items():
        if isinstance(value, str) and (Path(value).exists() or value.startswith("/")):
            # Keep as Path object for now, function can decide how to handle
            resolved[key] = Path(value)
        else:
            resolved[key] = value

    return resolved


def serialize_result(result: Any, output_path: Path) -> None:
    """
    Serialize function result to a file.

    Args:
        result: Function result to serialize
        output_path: Path to write result
    """
    # Handle numpy arrays (common in image processing)
    try:
        import numpy as np

        if isinstance(result, np.ndarray):
            # Save as .npy file
            np.save(str(output_path.with_suffix(".npy")), result)
            print(f"Saved numpy array to {output_path.with_suffix('.npy')}")
            return
    except ImportError:
        pass

    # Handle PIL images
    try:
        from PIL import Image

        if isinstance(result, Image.Image):
            result.save(output_path.with_suffix(".png"))
            print(f"Saved PIL Image to {output_path.with_suffix('.png')}")
            return
    except ImportError:
        pass

    # Handle JSON-serializable types
    try:
        with output_path.with_suffix(".json").open("w") as f:
            json.dump(result, f, indent=2)
        print(f"Saved result to {output_path.with_suffix('.json')}")
        return
    except (TypeError, ValueError):
        pass

    # Fallback: save string representation
    output_path.with_suffix(".txt").write_text(str(result))
    print(f"Saved string representation to {output_path.with_suffix('.txt')}")


def main():
    """Main entry point for the execution shim."""
    parser = argparse.ArgumentParser(description="Execute an introspected function")

    parser.add_argument("--module", required=True, help="Module name (e.g., skimage.filters)")
    parser.add_argument("--function", required=True, help="Function name to execute")
    parser.add_argument("--args-file", required=True, help="Path to JSON file with function arguments")
    parser.add_argument("--output", default="result", help="Output path for result (default: result)")
    parser.add_argument("--source", help="Package source to resolve before importing")

    args = parser.parse_args()

    try:
        # Resolve package source if provided
        if args.source:
            from .resolver import PackageResolver, PackageSource

            source = PackageSource.from_string(args.source)
            resolver = PackageResolver()
            resolved_path = resolver.resolve(source)
            import_path = resolver.get_import_path(resolved_path)
            sys.path.insert(0, str(import_path))

        # Import the module
        try:
            module = importlib.import_module(args.module)
        except ImportError as e:
            print(f"Error: Failed to import module '{args.module}': {e}", file=sys.stderr)
            sys.exit(1)

        # Get the function
        try:
            func = getattr(module, args.function)
        except AttributeError:
            print(f"Error: Function '{args.function}' not found in module '{args.module}'", file=sys.stderr)
            sys.exit(1)

        # Load arguments
        args_file = Path(args.args_file)
        if not args_file.exists():
            print(f"Error: Arguments file '{args.args_file}' not found", file=sys.stderr)
            sys.exit(1)

        func_args = load_args_from_file(args_file)
        func_args = resolve_file_paths(func_args)

        # Execute the function
        print(f"Executing {args.module}.{args.function}...")
        try:
            result = func(**func_args)
        except TypeError as e:
            print(f"Error: Failed to execute function: {e}", file=sys.stderr)
            print(f"Arguments provided: {list(func_args.keys())}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error during function execution: {e}", file=sys.stderr)
            import traceback

            traceback.print_exc()
            sys.exit(1)

        # Serialize result
        output_path = Path(args.output)
        serialize_result(result, output_path)

        print("Execution completed successfully")

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
