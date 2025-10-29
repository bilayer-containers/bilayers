"""Scaffolding utilities for generating Bilayers specs from introspection metadata."""

from typing import Optional
from pathlib import Path
from .discovery import FunctionMetadata
from .resolver import PackageSource


def _map_type_to_widget(annotation: str, param_name: str = "", docstring: str = "", has_default: bool = False) -> tuple[str, str]:
    """
    Map a type annotation to a Bilayers input type and widget hint.

    Args:
        annotation: Type annotation string
        param_name: Parameter name (used for heuristics)
        docstring: Function docstring (to extract type info)
        has_default: Whether the parameter has a default value

    Returns:
        Tuple of (input_type, widget_type) or ("skip", "") to skip the parameter
    """
    annotation = annotation.lower()
    param_name_lower = param_name.lower()
    docstring_lower = docstring.lower()

    # Parse docstring for type hints if annotation is "Any"
    # Look for patterns like "param_name : type" in docstring
    if annotation == "any" and param_name and docstring:
        import re
        # Match parameter documentation: param_name : type
        pattern = rf"{re.escape(param_name)}\s*:\s*(\w+)"
        match = re.search(pattern, docstring_lower)
        if match:
            doc_type = match.group(1)
            annotation = doc_type

    # Output parameters (optional pre-allocated arrays) - skip these entirely
    # These are advanced optimization parameters that users rarely need
    if param_name_lower in ["out", "output", "destination", "dst"] and has_default and "ndarray" in annotation:
        return ("skip", "")

    # Boolean types
    if "bool" in annotation:
        return ("checkbox", "checkbox")

    # Numeric types
    if "int" in annotation:
        return ("integer", "slider")
    if "float" in annotation or "number" in annotation or "scalar" in annotation:
        return ("float", "slider")

    # File/array types (common in image processing)
    if "ndarray" in annotation or "array" in annotation:
        return ("file", "file_upload")

    # String types (use 'textbox' to match Bilayers template)
    if "str" in annotation:
        return ("textbox", "textbox")

    # Path types
    if "path" in annotation:
        return ("file", "file_upload")

    # Heuristics based on parameter name
    # Common data input parameter names should be treated as file inputs
    if param_name_lower in ["image", "img", "data", "input", "file"]:
        return ("file", "file_upload")

    # Default (use 'textbox' to match Bilayers template)
    return ("textbox", "textbox")


def scaffold_spec(func_metadata: FunctionMetadata, source: Optional[str] = None) -> str:
    """
    Generate a Bilayers YAML spec from function metadata.

    Args:
        func_metadata: Function metadata from introspection
        source: Optional package source string

    Returns:
        YAML spec content as string
    """
    lines = []

    # Header
    lines.append(f"# Auto-generated Bilayers spec for {func_metadata.module}.{func_metadata.name}")
    lines.append(f"# Generated from introspection")
    if source:
        lines.append(f"# Source: {source}")
    lines.append("")

    # Citations (optional but good practice)
    lines.append("citations:")
    lines.append(f"  - name: \"{func_metadata.name}\"")
    if func_metadata.docstring:
        description = func_metadata.docstring.split("\n")[0]
        lines.append(f'    description: "{description}"')
    lines.append("")

    # Docker image info
    lines.append("docker_image:")
    lines.append("  org: bilayer")
    lines.append(f"  name: {func_metadata.name}")
    lines.append('  tag: "1.0.0"')
    lines.append('  platform: "linux/amd64"')
    lines.append("")

    # Algorithm folder name
    lines.append(f"algorithm_folder_name: \"{func_metadata.name}\"")
    lines.append("")

    # Exec function
    lines.append("exec_function:")
    lines.append('  name: "generate_cli_command"')
    lines.append(f'  cli_command: "python -m {func_metadata.name}"')
    lines.append("  hidden_args:")
    lines.append("    - cli_tag: --output_dir")
    lines.append('      value: "output"')
    lines.append("      cli_order: -1")
    lines.append("")

    # Introspection metadata (for reference)
    lines.append("# Introspection metadata")
    lines.append("# introspection:")
    lines.append(f"#   module: {func_metadata.module}")
    lines.append(f"#   function: {func_metadata.name}")
    if source:
        lines.append(f"#   source: {source}")
    lines.append("")

    # Inputs section
    has_file_inputs = False
    for param in func_metadata.parameters:
        input_type, _ = _map_type_to_widget(param.annotation, param.name, func_metadata.docstring, bool(param.default))
        if input_type == "file":
            has_file_inputs = True
            break

    if has_file_inputs:
        lines.append("inputs:")
        for param in func_metadata.parameters:
            input_type, widget_type = _map_type_to_widget(param.annotation, param.name, func_metadata.docstring, bool(param.default))
            if input_type == "skip":
                continue
            if input_type == "file":
                lines.append(f"  - name: {param.name}")
                lines.append(f"    type: {input_type}")
                lines.append(f'    label: "{param.name.replace("_", " ").title()}"')
                lines.append(f'    description: "Input {param.name}"')
                lines.append(f'    folder_name: "{param.name}_input"')
                lines.append(f'    cli_tag: "--{param.name}"')
                lines.append("    cli_order: 0")
                lines.append("    optional: False" if not param.default else "    optional: True")
                lines.append('    section_id: "inputs"')
                lines.append('    mode: "beginner"')
                if param.annotation != "Any":
                    lines.append(f"    # Type hint: {param.annotation}")
                lines.append("")
        lines.append("")

    # Parameters section
    has_params = False
    for param in func_metadata.parameters:
        input_type, _ = _map_type_to_widget(param.annotation, param.name, func_metadata.docstring, bool(param.default))
        if input_type != "file" and input_type != "skip":
            has_params = True
            break

    if has_params:
        lines.append("parameters:")
        for param in func_metadata.parameters:
            input_type, widget_type = _map_type_to_widget(param.annotation, param.name, func_metadata.docstring, bool(param.default))
            if input_type == "skip":
                continue
            if input_type != "file":
                lines.append(f"  - name: {param.name}")
                lines.append(f"    type: {input_type}")
                lines.append(f'    label: "{param.name.replace("_", " ").title()}"')
                lines.append(f'    description: "Parameter {param.name}"')

                if param.default:
                    lines.append(f"    default: {param.default}")
                else:
                    # Provide sensible defaults
                    if input_type == "integer":
                        lines.append("    default: 1")
                    elif input_type == "float":
                        lines.append("    default: 1.0")
                    elif input_type == "checkbox":
                        lines.append("    default: false")
                    elif input_type == "textbox":
                        lines.append('    default: ""')

                lines.append(f'    cli_tag: "--{param.name}"')
                lines.append("    optional: False" if not param.default else "    optional: True")
                lines.append('    section_id: "input-args"')
                lines.append('    mode: "beginner"')

                if param.annotation != "Any":
                    lines.append(f"    # Type hint: {param.annotation}")

                lines.append("")

    # Outputs section
    lines.append("outputs:")
    lines.append("  - name: result")

    # Try to infer output type from return annotation
    return_type = func_metadata.return_annotation.lower()
    if "ndarray" in return_type or "array" in return_type:
        lines.append("    type: file")
        lines.append('    label: "Output Result"')
        lines.append('    description: "Output array/image"')
    else:
        lines.append("    type: file")
        lines.append('    label: "Output Result"')
        lines.append('    description: "Function result"')

    lines.append('    cli_tag: "None"')
    lines.append("    cli_order: 0")
    lines.append("    optional: False")
    lines.append('    section_id: "outputs"')
    lines.append('    mode: "beginner"')
    lines.append("")

    # Display only section (empty but required)
    lines.append("display_only:")

    return "\n".join(lines)


def generate_algorithm_python_module(func_metadata: FunctionMetadata, source_str: str) -> str:
    """
    Generate a Python module that wraps the discovered function.

    Args:
        func_metadata: Function metadata
        source_str: Package source string

    Returns:
        Python module content as string
    """
    lines = [
        f'"""Wrapper module for {func_metadata.module}.{func_metadata.name}"""',
        "",
        "import argparse",
        "import sys",
        "import os",
        "from pathlib import Path",
        "import numpy as np",
        f"from {func_metadata.module} import {func_metadata.name}",
        "",
        "",
        "def load_image(path):",
        '    """Load image from various formats (TIFF, PNG, JPG, OME-TIFF)"""',
        "    try:",
        "        # Try tifffile first (handles OME-TIFF, regular TIFF)",
        "        import tifffile",
        "        return tifffile.imread(path)",
        "    except:",
        "        pass",
        "    ",
        "    try:",
        "        # Fall back to imageio (handles PNG, JPG, etc.)",
        "        import imageio.v3 as iio",
        "        return iio.imread(path)",
        "    except:",
        "        pass",
        "    ",
        "    try:",
        "        # Last resort: skimage.io",
        "        from skimage import io as skio",
        "        return skio.imread(path)",
        "    except Exception as e:",
        '        raise ValueError(f"Failed to load image {path}: {e}")',
        "",
        "",
        "def save_image(path, data):",
        '    """Save image to TIFF format"""',
        "    try:",
        "        import tifffile",
        "        tifffile.imwrite(path, data)",
        "    except:",
        "        # Fall back to imageio",
        "        import imageio.v3 as iio",
        "        iio.imwrite(path, data)",
        "",
        "",
        "def main():",
        '    """CLI entry point"""',
        "    parser = argparse.ArgumentParser(",
        f'        description="{func_metadata.docstring.split(chr(10))[0] if func_metadata.docstring else f"Run {func_metadata.name}"}"',
        "    )",
        "",
    ]

    # Identify file inputs
    file_inputs = []
    for param in func_metadata.parameters:
        input_type, _ = _map_type_to_widget(param.annotation, param.name, func_metadata.docstring, bool(param.default))
        if input_type == "file":
            file_inputs.append(param.name)

    # Add arguments based on function parameters
    for param in func_metadata.parameters:
        input_type, _ = _map_type_to_widget(param.annotation, param.name, func_metadata.docstring, bool(param.default))

        # Skip parameters marked as skip
        if input_type == "skip":
            continue

        # Determine argparse type
        if input_type == "file":
            param_type = "str"
        elif input_type == "integer":
            param_type = "int"
        elif input_type == "float":
            param_type = "float"
        elif input_type == "checkbox":
            param_type = "lambda x: x.lower() in ['true', '1', 'yes']"
        else:
            param_type = "str"

        if param.default:
            lines.append(f'    parser.add_argument("--{param.name}", type={param_type}, default={param.default}, help="{param.name} parameter")')
        else:
            lines.append(f'    parser.add_argument("--{param.name}", type={param_type}, required=True, help="{param.name} parameter")')

    # Add output directory argument
    lines.extend([
        '    parser.add_argument("--output_dir", type=str, default="./output", help="Output directory for results")',
        "",
        "    args = parser.parse_args()",
        "",
        "    # Create output directory",
        "    os.makedirs(args.output_dir, exist_ok=True)",
        "",
    ])

    # Load file inputs
    if file_inputs:
        lines.append("    # Load input files")
        for file_param in file_inputs:
            lines.extend([
                f"    {file_param}_path = args.{file_param}",
                f"    if os.path.isdir({file_param}_path):",
                f"        # If directory, get first file",
                f"        files = [f for f in os.listdir({file_param}_path) if os.path.isfile(os.path.join({file_param}_path, f))]",
                f"        if not files:",
                f'            raise ValueError(f"No files found in {{args.{file_param}}}")',
                f"        {file_param}_path = os.path.join({file_param}_path, files[0])",
                f'    print(f"Loading {file_param}: {{{file_param}_path}}")',
                f"    {file_param}_data = load_image({file_param}_path)",
                f'    print(f"  Shape: {{{file_param}_data.shape}}, dtype: {{{file_param}_data.dtype}}")',
                "",
            ])

    lines.extend([
        "    # Call the function",
        f'    print(f"\\nRunning {func_metadata.name}...")',
        f"    result = {func_metadata.name}(",
    ])

    # Add function call arguments
    func_params = [p for p in func_metadata.parameters
                   if _map_type_to_widget(p.annotation, p.name, func_metadata.docstring, bool(p.default))[0] != "skip"]

    for i, param in enumerate(func_params):
        comma = "," if i < len(func_params) - 1 else ""
        input_type, _ = _map_type_to_widget(param.annotation, param.name, func_metadata.docstring, bool(param.default))

        if input_type == "file":
            lines.append(f"        {param.name}={param.name}_data{comma}")
        else:
            lines.append(f"        {param.name}=args.{param.name}{comma}")

    lines.extend([
        "    )",
        f'    print(f"  Result shape: {{result.shape}}, dtype: {{result.dtype}}")',
        "",
        "    # Save result",
        f'    print(f"\\nSaving result...")',
        "    output_path = os.path.join(args.output_dir, 'result.tif')",
        "    save_image(output_path, result)",
        f'    print(f"✓ Result saved to {{output_path}}")',
        '    return 0',
        "",
        "",
        'if __name__ == "__main__":',
        "    sys.exit(main())",
        "",
    ])

    return "\n".join(lines)


def generate_algorithm_dockerfile(func_metadata: FunctionMetadata, source_str: str, python_version: str = "3.11") -> str:
    """
    Generate a Dockerfile for the algorithm base image.

    Args:
        func_metadata: Function metadata
        source_str: Package source string
        python_version: Python version to use

    Returns:
        Dockerfile content as string
    """
    source = PackageSource.from_string(source_str)

    lines = [
        f"# Algorithm base Docker image for {func_metadata.name}",
        f"FROM python:{python_version}-slim",
        "",
        "# Set working directory",
        "WORKDIR /bilayers",
        "",
    ]

    # Install image I/O libraries (support for TIFF, PNG, JPG, OME-TIFF)
    lines.append("# Install image I/O libraries")
    lines.append('RUN pip install --no-cache-dir tifffile imageio numpy')
    lines.append("")

    # Install the target package based on source type
    if source.source_type.value == "pypi":
        package_spec = source.location
        if source.version:
            package_spec += f"=={source.version}"
        lines.append("# Install algorithm package from PyPI")
        lines.append(f'RUN pip install --no-cache-dir "{package_spec}"')
    elif source.source_type.value == "git":
        git_url = source.location
        if source.ref:
            git_url += f"@{source.ref}"
        lines.append("# Install git for package installation")
        lines.append("RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*")
        lines.append("# Install algorithm package from Git")
        lines.append(f'RUN pip install --no-cache-dir "git+{git_url}"')
    elif source.source_type.value == "local":
        lines.append("# Copy and install local package")
        lines.append("COPY package /bilayers/package")
        lines.append("RUN pip install --no-cache-dir /bilayers/package")

    lines.extend([
        "",
        "# Copy algorithm wrapper module",
        f"COPY {func_metadata.name}.py /bilayers/{func_metadata.name}.py",
        "",
        "# Default command",
        'CMD ["python"]',
        "",
    ])

    return "\n".join(lines)


def generate_init_file() -> str:
    """Generate __init__.py for algorithm folder."""
    return """import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
"""


def scaffold_algorithm_folder(
    func_metadata: FunctionMetadata,
    source: str,
    output_dir: Path,
    python_version: str = "3.11"
) -> Path:
    """
    Generate a complete algorithm folder structure.

    Args:
        func_metadata: Function metadata
        source: Package source string
        output_dir: Output directory for the algorithm folder
        python_version: Python version for Dockerfile

    Returns:
        Path to the created algorithm folder
    """
    # Create algorithm folder
    algo_folder = output_dir / func_metadata.name
    algo_folder.mkdir(parents=True, exist_ok=True)

    # Generate config.yaml
    config_content = scaffold_spec(func_metadata, source)
    (algo_folder / "config.yaml").write_text(config_content)

    # Generate Python module
    module_content = generate_algorithm_python_module(func_metadata, source)
    (algo_folder / f"{func_metadata.name}.py").write_text(module_content)

    # Generate __main__.py (makes module runnable with python -m)
    main_content = f"""from .{func_metadata.name} import main

if __name__ == "__main__":
    main()
"""
    (algo_folder / "__main__.py").write_text(main_content)

    # Generate Dockerfile
    dockerfile_content = generate_algorithm_dockerfile(func_metadata, source, python_version)
    (algo_folder / "Dockerfile").write_text(dockerfile_content)

    # Generate __init__.py
    (algo_folder / "__init__.py").write_text(generate_init_file())

    return algo_folder
