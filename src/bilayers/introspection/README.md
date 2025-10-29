# Bilayers Module Introspection

This module provides utilities for discovering callable functions in Python libraries and automatically scaffolding Bilayers specifications for them.

## Features

- **Discovery**: Enumerate public callables from Python modules with metadata extraction
- **Package Resolution**: Support for local, PyPI, and Git package sources
- **Scaffolding**: Auto-generate Bilayers YAML specs from introspection results
- **Execution**: Runtime shim for invoking discovered functions
- **Local Development**: Automatically bundles local bilayers source into Docker images (no PyPI dependency)

## Usage

### Docker-Based Discovery

Discover functions in an isolated Docker container:

```bash
bilayers_cli discover skimage.filters \
  --source "pypi:scikit-image" \
  --filter "gaussian" \
  --output functions.json
```

This approach:
- Requires NO local installation of the target library
- Isolates all dependencies in a container
- Automatically builds and cleans up temporary images

### Build Algorithm Container

Build a production Docker image for a discovered algorithm:

```bash
bilayers_cli build-algorithm ./specs/gaussian.yaml \
  --source "pypi:scikit-image" \
  --image-name "my-algorithm" \
  --tag "1.0.0"
```

### Local Discovery (Alternative)

If you have the library installed locally:

```bash
bilayers_cli discover skimage.filters --format json
bilayers_cli scaffold skimage.filters gaussian -o ./specs
```

### Package Sources

Support for multiple package sources:

```bash
# PyPI with version
--source "pypi:scikit-image==0.21.0"

# Local path
--source "local:/path/to/my/package"

# Git repository
--source "git:https://github.com/user/repo@main"
```

## Module Structure

```
introspection/
├── __init__.py          # Package exports
├── discovery.py         # Function discovery and metadata extraction
├── resolver.py          # Package source resolution
├── scaffold.py          # YAML spec generation
├── exec.py             # Runtime execution shim
└── __main__.py         # CLI entry point
```

## Python API

```python
from bilayers.introspection import discover_callables, PackageSource, PackageResolver

# Discover functions
results = discover_callables("skimage.filters", filter_pattern="gaussian")

# Resolve package
source = PackageSource.from_string("pypi:scikit-image==0.21.0")
resolver = PackageResolver()
resolved_path = resolver.resolve(source)
```

## Testing

Run the introspection test suite:

```bash
pytest tests/introspection/ -v
```

## Implementation Status

- ✅ Discovery utilities with signature inspection
- ✅ Package source resolution (local/PyPI/Git)
- ✅ CLI integration (discover, scaffold, build-algorithm)
- ✅ Execution shim for runtime invocation
- ✅ Comprehensive test coverage
- ✅ Docker containerization workflow
- ✅ Python version selection (3.9, 3.10, 3.11, 3.12)
- ⏳ Gradio/Jupyter template integration
- ⏳ Caching and metadata versioning

## Architecture

### Docker Build Flow

1. **Copy Local Bilayers**: Entire project (src/, pyproject.toml) copied to build context
2. **Install Bilayers**: `pip install /path/to/bilayers` in container
3. **Install Target Package**: From PyPI, Git, or local source
4. **Run Discovery/Algorithm**: Execute introspection or serve interface

This approach:
- ✅ No PyPI dependency for bilayers
- ✅ Uses your current local code
- ✅ Easy to test changes

### Discovery Flow

1. **Import Module**: Dynamically load the target module in container
2. **Enumerate Callables**: Use `inspect` to find functions
3. **Extract Metadata**: Capture signatures, type hints, docstrings
4. **Serialize Results**: Output as JSON or Markdown

### Scaffolding Flow

1. **Load Metadata**: From discovery results JSON
2. **Map Types**: Convert type hints to Bilayers input/parameter types
3. **Generate YAML**: Construct spec with execution configuration
4. **Write Output**: Save to specified directory (default: `./specs`)

### Execution Flow

1. **Parse Args**: Load function arguments from JSON
2. **Resolve Paths**: Handle file inputs and parameter marshaling
3. **Invoke Function**: Call the discovered function with resolved args
4. **Serialize Output**: Save results (numpy arrays, images, JSON)

## Future Enhancements

- Widget customization via config overrides
- Discovery result caching with version tracking
- Integration with existing Bilayers generators
- Container image building for introspected functions
- Support for complex return types and multi-output functions
