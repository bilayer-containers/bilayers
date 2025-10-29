---
title: Module Introspection
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

The Bilayers module introspection feature allows you to automatically discover functions from Python libraries (like scikit-image, scipy, etc.) and generate ready-to-run Docker containers without manual installation or configuration.

## What is Module Introspection?

Module introspection automatically:
- **Discovers** callable functions in Python modules using isolated Docker containers
- **Generates** Bilayers YAML specifications from function metadata
- **Builds** production-ready Docker images with all dependencies bundled
- **Serves** interactive Gradio/Jupyter interfaces

**Key Benefit**: No local installation of target libraries required. Everything runs in isolated Docker containers.

## Prerequisites

1. **Bilayers project cloned locally**

    For quick environment setup it is suggested to use `pixi`:

    ```bash
    curl -fsSL https://pixi.sh/install.sh | sh

    # wget if you don't have curl
    wget -qO- https://pixi.sh/install.sh | sh


    git clone https://github.com/bilayer-containers/bilayers.git
    cd bilayers
    pixi shell -e dev
   ```

   The introspection feature automatically includes the local bilayers source in Docker images, so you don't need bilayers published to PyPI.

2. **Docker installed and running**
   - For Mac: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
   - For Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)

   Verify Docker is running:
   ```bash
   docker --version
   ```

That's it! No need to install scikit-image, scipy, or any other target library locally.

## Quick Start

### Workspace Structure

Module introspection uses two main directories:

```
.introspection/
└── discovery.json              # Discovery results from 'discover' command

algorithms/                      # Algorithm folders from 'scaffold' command
├── gaussian/
│   ├── config.yaml             # Bilayers spec
│   ├── Dockerfile              # Algorithm base image
│   ├── gaussian.py             # Python wrapper module
│   └── __init__.py
├── butter/
│   ├── config.yaml
│   ├── Dockerfile
│   ├── butter.py
│   └── __init__.py
└── ...
```

- `./.introspection/` is automatically added to `.gitignore`
- `./algorithms/` contains complete, ready-to-build algorithm folders following Bilayers conventions

### Complete Workflow

```bash
# 1. Discover functions
bilayers_cli discover skimage.filters \
  --source "pypi:scikit-image" \
  --filter "gaussian"

# 2. Generate algorithm folder
bilayers_cli scaffold gaussian \
  --source "pypi:scikit-image"

# 3. Build and serve with Docker
./scripts/build_docker.sh --algorithm gaussian --interface gradio
docker run -it --rm -p 7878:7878 bilayer/gaussian:1.0.0-gradio
```

Open your browser to `http://localhost:7878`.

**What happens:**
- `discover` finds functions in Docker container, saves to `./.introspection/discovery.json`
- `scaffold` generates complete algorithm folder at `./algorithms/gaussian/`
- `build_docker.sh` builds both the algorithm base image and wrapper interface image
- `docker run` serves the Gradio interface on port 7878

**Note:** `build_docker.sh` automatically builds the algorithm base image, generates interface files, and builds the wrapper image - all in one command!

## Command Reference

### 1. discover

Discover callable functions in a Docker container.

```bash
bilayers_cli discover MODULE \
  --source SOURCE \
  [--filter PATTERN] \
  [--output FILE] \
  [--python-version VERSION] \
  [--include-private] \
  [--keep-image]
```

**Arguments:**
- `MODULE`: Python module to introspect (e.g., `skimage.filters`)
- `--source`: **Required**. Package source (see Package Sources below)
- `--filter`: Regex pattern to filter function names
- `--output`, `-o`: Save results to JSON file (default: `./.introspection/discovery.json`)
- `--python-version`: Python version to use (default: `3.11`)
  - Supported: `3.9`, `3.10`, `3.11`, `3.12`
- `--include-private`: Include functions starting with `_`
- `--keep-image`: Don't delete the Docker image after discovery

**Example:**
```bash
bilayers_cli discover skimage.filters \
  --source "pypi:scikit-image==0.21.0" \
  --filter "gaussian|median|sobel" \
  --python-version "3.10"
```

**Output:**
```
Building introspection Docker image for scikit-image (Python 3.10)...
Built image: bilayers-introspect:introspect
Discovering functions in skimage.filters...

Discovered 3 functions:
  - gaussian(image, sigma=1, *, mode='nearest', cval=0, ...)
  - median(image, footprint=None, *, mode='reflect', ...)
  - sobel(image, *, axis=None, mode='reflect', cval=0.0)

Cleaning up image bilayers-introspect:introspect...
Results saved to ./.introspection/discovery.json
```

### 2. scaffold

Generate a complete algorithm folder with Dockerfile, config.yaml, and Python module.

```bash
bilayers_cli scaffold [DISCOVERY_JSON] FUNCTION_NAME \
  --source SOURCE \
  [--output DIR] \
  [--python-version VERSION]
```

**Arguments:**
- `DISCOVERY_JSON`: Path to discovery JSON file (default: `./.introspection/discovery.json`)
- `FUNCTION_NAME`: Name of function to scaffold
- `--source`: **Required**. Package source (must match discovery source)
- `--output`, `-o`: Output directory for algorithm folder (default: `./algorithms`)
- `--python-version`: Python version for Dockerfile (default: `3.11`)

**Example (using defaults):**
```bash
# Uses ./.introspection/discovery.json and outputs to ./algorithms/gaussian/
bilayers_cli scaffold gaussian \
  --source "pypi:scikit-image==0.21.0"
```

**Example (custom paths):**
```bash
bilayers_cli scaffold ./my_discovery.json gaussian \
  --source "pypi:scikit-image==0.21.0" \
  --output ./my_algorithms \
  --python-version "3.10"
```

**Output:**
```
Generated algorithm folder for gaussian at ./algorithms/gaussian

Folder structure:
  ./algorithms/gaussian/
    ├── config.yaml
    ├── Dockerfile
    ├── gaussian.py
    └── __init__.py
```

### 3. build-algorithm (Optional - for advanced use)

Build the algorithm base Docker image from the generated algorithm folder.

**Note:** You typically don't need to run this command directly. The `build_docker.sh` script (recommended workflow) builds the algorithm base image automatically.

```bash
bilayers_cli build-algorithm [ALGORITHM_FOLDER] \
  --image-name NAME \
  [--function-name FUNCTION] \
  [--tag TAG]
```

**Arguments:**
- `ALGORITHM_FOLDER`: Path to algorithm folder (optional if using `--function-name`)
- `--image-name`: **Required**. Docker image name
- `--function-name`: Function name (automatically uses `./algorithms/{function_name}/`)
- `--tag`: Image tag (default: `latest`)

**Example:**
```bash
# Manually build just the algorithm base image
bilayers_cli build-algorithm \
  --function-name gaussian \
  --image-name "gaussian-filter" \
  --tag "1.0.0"
```

This is only needed if you want to build the base image separately for testing or custom workflows.

## Package Sources

Three types of package sources are supported:

### PyPI Packages
```bash
--source "pypi:PACKAGE_NAME"
--source "pypi:PACKAGE_NAME==VERSION"
```

**Examples:**
```bash
--source "pypi:scikit-image"
--source "pypi:scikit-image==0.21.0"
--source "pypi:scipy==1.11.0"
```

### Local Packages
```bash
--source "local:/absolute/path/to/package"
```

**Example:**
```bash
--source "local:/home/user/my-custom-library"
```

### Git Repositories
```bash
--source "git:REPO_URL"
--source "git:REPO_URL@BRANCH_OR_TAG"
```

**Examples:**
```bash
--source "git:https://github.com/user/repo"
--source "git:https://github.com/user/repo@main"
--source "git:https://github.com/user/repo@v1.0.0"
```

## Python Version Selection

Choose the Python version for your Docker containers:

```bash
# Use Python 3.9
bilayers_cli discover skimage.filters \
  --source "pypi:scikit-image" \
  --python-version "3.9"

# Use Python 3.12
bilayers_cli build-algorithm ./specs/gaussian.yaml \
  --source "pypi:scikit-image" \
  --image-name "gaussian" \
  --python-version "3.12"
```

**Supported versions:** `3.9`, `3.10`, `3.11` (default), `3.12`

## Complete Example: scipy.signal.butter

```bash
# Step 1: Discover signal processing functions
bilayers_cli discover scipy.signal \
  --source "pypi:scipy==1.11.0" \
  --filter "butter|cheby"

# Step 2: Generate algorithm folder
bilayers_cli scaffold butter \
  --source "pypi:scipy==1.11.0"

# Step 3: Build and serve
./scripts/build_docker.sh --algorithm butter --interface gradio
docker run -it --rm -p 7878:7878 bilayer/butter:gradio-latest
```

Open your browser to `http://localhost:7878`.

**Workspace structure after running these commands:**
```
./.introspection/
└── discovery.json           # Discovery results

algorithms/
└── butter/
    ├── config.yaml          # Bilayers spec
    ├── Dockerfile           # Algorithm base image
    ├── butter.py            # Python wrapper module
    ├── __init__.py
    └── generated_folders/   # Created by generate command
        └── gradio/
            └── app.py       # Gradio interface
```

## How It Works

### Docker Image Building

**For Discovery (`discover`):**

The system creates a minimal Docker image that:
1. **Embeds a standalone discovery script** (no bilayers dependency)
2. **Installs only the target package** from your specified source
3. **Runs discovery and saves results**

This keeps discovery images small and fast!

**For Algorithm Building (`build-algorithm`):**

The system:
1. **Copies your local bilayers project** into the Docker build context
   - Includes `src/`, `pyproject.toml`, and all dependencies
   - Excludes `.git`, `__pycache__`, `.pixi` to keep builds fast

2. **Installs bilayers from the local copy**
   ```dockerfile
   COPY bilayers /bilayers/bilayers
   RUN pip install --no-cache-dir /bilayers/bilayers
   ```

3. **Installs the target package** from your specified source

4. **Bundles the algorithm spec** for serving

This means:
- ✅ Discovery doesn't need bilayers (fast & minimal)
- ✅ Algorithm images use your current local bilayers code
- ✅ No PyPI dependency required
- ✅ Easy to test changes before committing

### Workflow Diagram

```
┌──────────────────────────────────────────────────┐
│  1. discover                                      │
│  Builds minimal container (no bilayers)          │
│  → discovers functions → saves to                │
│     ./.introspection/discovery.json              │
└─────────────┬────────────────────────────────────┘
              │ ./.introspection/discovery.json
              ▼
┌──────────────────────────────────────────────────┐
│  2. scaffold                                      │
│  Reads discovery.json → generates complete       │
│  algorithm folder with Dockerfile, config.yaml,  │
│  and Python wrapper module                       │
└─────────────┬────────────────────────────────────┘
              │ ./algorithms/{function}/
              ▼
┌──────────────────────────────────────────────────┐
│  3. build-algorithm                               │
│  Builds algorithm base Docker image from         │
│  Dockerfile in algorithm folder                  │
└─────────────┬────────────────────────────────────┘
              │ Algorithm base image
              ▼
┌──────────────────────────────────────────────────┐
│  4. build_docker.sh OR manual docker build        │
│  - Generates interface files (app.py, etc.)      │
│  - Builds wrapper image with Gradio/Jupyter      │
│  - Layers on top of algorithm base image         │
└─────────────┬────────────────────────────────────┘
              │ Complete wrapper image
              ▼
┌──────────────────────────────────────────────────┐
│  5. docker run                                    │
│  Serve containerized Gradio/Jupyter interface    │
│  Access at http://localhost:7860                 │
└──────────────────────────────────────────────────┘
```

**Workspace organization:**
```
project/
├── .introspection/          # ← Discovery results (gitignored)
│   └── discovery.json
├── algorithms/              # ← Algorithm folders
│   ├── gaussian/
│   │   ├── config.yaml      # ← Bilayers spec
│   │   ├── Dockerfile       # ← Algorithm base image
│   │   ├── gaussian.py      # ← Python wrapper
│   │   ├── __init__.py
│   │   └── generated_folders/  # ← Generated by bilayers_cli
│   │       └── gradio/
│   │           └── app.py
│   └── butter/
│       ├── config.yaml
│       ├── Dockerfile
│       └── ...
└── ... (your project files)
```

## Serving via Docker

After scaffolding your algorithm folder, use `build_docker.sh` to build and serve:

```bash
# Build everything (base image + wrapper image) in one command
./scripts/build_docker.sh --algorithm gaussian --interface gradio

# Run the complete stack
docker run -it --rm -p 7860:7860 bilayer/gaussian:gradio-latest
```

**What it does:**
- Builds the algorithm base image (from `./algorithms/gaussian/Dockerfile`)
- Generates the interface files
- Builds the wrapper image with Gradio/Jupyter
- All in one automated script

**Note:** You don't need to run `bilayers_cli build-algorithm` separately - `build_docker.sh` handles everything!

### Docker Run Options

```bash
# Run interactively
docker run -it --rm -p 7860:7860 <image-name>

# Run in background (detached)
docker run -d --rm -p 7860:7860 <image-name>

# Custom port mapping (host:container)
docker run -it --rm -p 8080:7860 <image-name>

# Mount volumes for data
docker run -it --rm -p 7860:7860 \
  -v /path/to/data:/data \
  <image-name>

# Set environment variables
docker run -it --rm -p 7860:7860 \
  -e GRADIO_SERVER_PORT=7860 \
  <image-name>
```

### Understanding the Docker Layers

Bilayers uses a two-layer approach:

1. **Algorithm Base Image** (built by `build-algorithm`)
   - Contains the algorithm package (e.g., scikit-image)
   - Contains the wrapper Python module
   - Platform: `linux/amd64`

2. **Interface Wrapper Image** (built by `generate` + `docker build`)
   - Extends the base image
   - Adds Gradio/Jupyter dependencies
   - Adds the generated interface code
   - Configured to serve on port 7860

This layered approach allows you to:
- Build the algorithm base once
- Generate multiple interface types (Gradio, Jupyter) from the same base
- Update interfaces without rebuilding the algorithm

## Troubleshooting

### "Docker not found"
Ensure Docker is installed and running:
```bash
docker --version
docker ps
```

### "Failed to build Docker image"
Check:
- Docker daemon is running
- Sufficient disk space
- Network connection (for PyPI/Git sources)
- Package name and version are correct

### "Function not found in discovery results"
List available functions:
```bash
cat ./.introspection/discovery.json | grep '"name"'
```

Or use `--include-private` if the function starts with `_`

### Python version compatibility
If a package doesn't support a Python version:
```bash
# Try a different Python version
--python-version "3.10"
```

## Advanced: Using with Local Development

For local package development:

```bash
# Discover from local package
bilayers_cli discover mypackage.module \
  --source "local:/home/user/mypackage"

# Scaffold the function
bilayers_cli scaffold myfunction \
  --source "local:/home/user/mypackage"

# Build algorithm base image
bilayers_cli build-algorithm \
  --function-name myfunction \
  --image-name "my-local-algorithm"

# Build and serve via Docker
./scripts/build_docker.sh --algorithm myfunction --interface gradio
docker run -it --rm -p 7860:7860 bilayer/myfunction:gradio-latest
```

The local package will be copied into the Docker image during build.

## Next Steps

- See [Understanding Config](../custom_algorithm/understanding_config.md) to customize generated specs
- Check [Supported Interfaces](../custom_algorithm/supported_interfaces.md) for Gradio/Jupyter options
- Read [Steps to Run](./steps_to_run.md) for deploying Docker images

## Python API

For programmatic use:

```python
from bilayers.introspection.containerize import (
    build_introspection_image,
    discover_in_container,
    build_algorithm_image
)
from bilayers.introspection.resolver import PackageSource

# Build introspection image
source = PackageSource.from_string("pypi:scikit-image")
image_name = build_introspection_image(
    source,
    "my-introspect",
    python_version="3.11"
)

# Discover functions
results = discover_in_container(
    image_name,
    "skimage.filters",
    filter_pattern="gaussian"
)

print(f"Found {len(results)} functions")
```

## Getting Help

- Technical details: [introspection module README](../../src/bilayers/introspection/README.md)
- Report issues: [GitHub Issues](https://github.com/broadinstitute/bilayers/issues)
- Planning document: `.dev_plan/module_introspection_layer.md`
