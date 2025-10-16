Now I'll create a comprehensive restructuring plan based on the research:

# Bilayers Codebase Restructuring Plan

## Executive Summary

This plan details the complete restructuring of the bilayers codebase to achieve a unified library structure. The goal is to transform the current dual-package structure (separate `src/bilayers/` and `src/bilayers_cli/`) into a single, cohesive `bilayers` library with integrated CLI functionality.

## Current vs. Target Structure

### Current Structure:
```
├── src/bilayers/                    # Core bilayers package
│   ├── __init__.py
│   ├── algorithms/                  # Algorithm implementations
│   └── build/
│       ├── dockerfiles/             # Docker templates  
│       └── parse/
│           ├── parse.py             # Config parsing logic
│           ├── generate.py          # Interface generation logic
│           └── *.py.j2              # Jinja2 templates
├── src/bilayers_cli/               # Separate CLI package
│   ├── bilayers_cli/
│   │   ├── cli.py                   # CLI entry point
│   │   └── cli_generator.py         # CLI command generation
│   ├── tests/                       # CLI-specific tests
│   └── pyproject.toml               # CLI-specific config
├── pyproject.toml                   # Core bilayers config
└── noxfile.py                       # Build automation
```

### Target Structure:
```
├── algorithms/                      # MOVED: Algorithm implementations
├── interfaces/
│   ├── dockerfiles/                 # MOVED: Docker templates
│   └── templates/                   # MOVED: Jinja2 templates
├── src/bilayers/
│   ├── __init__.py                  # UPDATED: Helper functions
│   ├── parse.py                     # MOVED: Config parsing
│   ├── generate.py                  # MOVED: Interface generation
│   └── cli/
│       ├── __init__.py              # NEW: CLI module init
│       ├── cli.py                   # MOVED: CLI entry point
│       └── cli_generator.py         # MOVED: CLI generation
├── tests/                           # CONSOLIDATED: All tests
├── pyproject.toml                   # UNIFIED: Single config
└── noxfile.py                       # UPDATED: New paths
```

## Phase-by-Phase Restructuring Plan

### Phase 1: Pre-Restructuring Setup

#### 1.1: Create New Directory Structure
```bash
# Create new top-level directories
mkdir -p algorithms
mkdir -p interfaces/dockerfiles
mkdir -p interfaces/templates
mkdir -p src/bilayers/cli
mkdir -p tests/cli
```

#### 1.2: Unify pyproject.toml Configuration
**Action**: Replace top-level `pyproject.toml` with unified configuration

**New Unified pyproject.toml**:
```toml
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "bilayers"
version = "0.1.0"
description = "Specifications and automated interfaces for wrapped tools with integrated CLI"
authors = [
    {name = "Rajavi Shah", email = "shahraja@broadinstitute.org"},
    {name = "Nodar Gogoberidze", email = "gnodar01@gmail.com"},
    {name = "Beth Cimini", email = "bcimini@broadinstitute.org"}
]
maintainers = [
    {name = "Rajavi Shah", email = "shahraja@broadinstitute.org"},
    {name = "Nodar Gogoberidze", email = "gnodar01@gmail.com"},
    {name = "Beth Cimini", email = "bcimini@broadinstitute.org"}
]
readme = "README.md"
license = "BSD-3-Clause"
requires-python = ">=3.9"
dependencies = [
    "nox>=2024.4.15,<2025",
    "pyyaml>=6.0.1,<7",
]

[project.optional-dependencies]
docs = ["mystmd>=1.3.17,<2"]
dev = [
    "numpy", "scipy", "scikit-image", "jinja2", "nbformat", 
    "ipython", "ipywidgets", "gradio", "pytest", "ruff", "pyright",
    "pre-commit", "mypy", "types-pyyaml"
]

[project.scripts]
bilayers_cli = "bilayers.cli.cli:cli"

[tool.setuptools.packages.find]
where = ["src"]
include = ["bilayers*"]

[tool.pixi.project]
channels = ["conda-forge"]
platforms = ["win-64", "linux-64", "osx-64", "osx-arm64"]

[tool.pixi.dependencies]
python = ">=3.9"

[tool.pixi.pypi-dependencies]
bilayers = { path = ".", editable = true }

[tool.pixi.environments]
dev = ["dev", "docs"]

[tool.ruff]
line-length = 160  # Keep the more permissive setting

[tool.ruff.lint]
select = ["W", "F", "C", "E"]
extend-select = ["W291", "W292", "W293", "F401", "F823", "F841", "C901", "E501"]

[tool.pyright]
pythonVersion = "3.10"
```

### Phase 2: File Relocation

#### 2.1: Move Algorithms Directory
```bash
# Move algorithms to top level
mv src/bilayers/algorithms/* algorithms/
rmdir src/bilayers/algorithms
```

#### 2.2: Move Docker Templates
```bash
# Move dockerfiles
mv src/bilayers/build/dockerfiles/* interfaces/dockerfiles/
```

#### 2.3: Move Jinja2 Templates  
```bash
# Move template files
mv src/bilayers/build/parse/*.py.j2 interfaces/templates/
```

#### 2.4: Move Core Modules
```bash
# Move parsing and generation modules
mv src/bilayers/build/parse/parse.py src/bilayers/parse.py
mv src/bilayers/build/parse/generate.py src/bilayers/generate.py

# Clean up empty directories
rmdir src/bilayers/build/parse
rmdir src/bilayers/build
```

#### 2.5: Move CLI Modules
```bash
# Move CLI modules
mv src/bilayers_cli/bilayers_cli/cli.py src/bilayers/cli/cli.py  
mv src/bilayers_cli/bilayers_cli/cli_generator.py src/bilayers/cli/cli_generator.py

# Move CLI tests
mv src/bilayers_cli/tests/* tests/cli/

# Remove old CLI structure
rm -rf src/bilayers_cli
```

#### 2.6: Create CLI Module Init
**Create `src/bilayers/cli/__init__.py`**:
```python
"""
Bilayers CLI module providing command-line interface functionality.
"""

from .cli import cli
from .cli_generator import main

__all__ = ["cli", "main"]
```

### Phase 3: Update Import Statements and References

#### 3.1: Update src/bilayers/parse.py
**Changes needed**:
- Update fallback algorithm paths to use project root
- Ensure compatibility with new structure

**Specific changes**:
```python
# Line 91: Update fallback path
# FROM:
config_path = bilayers.package_path() / "algorithms/classical_segmentation/config.yaml"
# TO:  
config_path = bilayers.project_path() / "algorithms/classical_segmentation/config.yaml"

# Line 93: Update relative fallback path  
# FROM:
config_path = Path("../../../src/bilayers/algorithms/classical_segmentation/config.yaml")
# TO:
config_path = Path("algorithms/classical_segmentation/config.yaml")
```

#### 3.2: Update src/bilayers/generate.py
**Changes needed**:
- Fix imports from parse module
- Update template loading paths
- Use project root for template discovery

**Specific changes**:
```python
# Lines 6, 11: Fix imports
# FROM:
from parse import main as parse_config
from parse import InputOutput, Parameter, ExecFunction, Citations
# TO:
from bilayers.parse import main as parse_config  
from bilayers.parse import InputOutput, Parameter, ExecFunction, Citations

# Update template loading logic to use project root templates
# Lines 104, 150, etc.: Update Environment initialization
# FROM:
env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)), ...)
# TO:
import bilayers
template_dir = bilayers.project_path() / "interfaces/templates"
env = Environment(loader=FileSystemLoader(searchpath=str(template_dir)), ...)

# Lines 188, 201, 234, 252: Update template file references to just use filenames
# Templates will be loaded from the configured template directory
```

#### 3.3: Update src/bilayers/cli/cli.py
**Changes needed**:
- Update imports to use new module structure

**Specific changes**:
```python
# Line 3: Update import  
# FROM:
from bilayers.build.parse.parse import parse_config
# TO:
from bilayers.parse import parse_config

# Line 4: Update CLI generator import
# FROM:
from bilayers_cli.bilayers_cli.cli_generator import main
# TO: 
from bilayers.cli.cli_generator import main
```

#### 3.4: Update src/bilayers/cli/cli_generator.py
**Changes needed**:
- Update imports to use new module structure

**Specific changes**:
```python
# Line 3: Update import
# FROM:
from bilayers.build.parse.parse import Config, HiddenArgs  
# TO:
from bilayers.parse import Config, HiddenArgs
```

### Phase 4: Update Build and Configuration Files

#### 4.1: Update noxfile.py
**Critical changes needed**:

```python
# Update PKG_ROOT calculation
# FROM:
PKG_ROOT = Path(bilayers.__path__[0])  # Points to src/bilayers/
# TO: 
PKG_ROOT = Path(bilayers.__path__[0])  # Still points to src/bilayers/
PROJ_ROOT = (PKG_ROOT / "../..").resolve()  # Points to project root

# Update run_parse session (lines 104-107)
# FROM:
session.cd(PKG_ROOT/"build/parse") 
session.run("python", "parse.py", config_path)
# TO:
session.run("python", "-m", "bilayers.parse", config_path)

# Update run_generate session (lines 120-123)  
# FROM:
session.cd(PKG_ROOT/"build/parse")
session.run("python", "generate.py", config_path) 
# TO:
session.run("python", "-m", "bilayers.generate", config_path)

# Update build_algorithm session (line 147)
# FROM:
algorithm_path = PKG_ROOT / f"algorithms/{algorithm}"
# TO:
algorithm_path = PROJ_ROOT / f"algorithms/{algorithm}"

# Update config file path (line 170)
# FROM: 
config_file_path = PKG_ROOT/f"algorithms/{algorithm}/config.yaml"
# TO:
config_file_path = PROJ_ROOT / f"algorithms/{algorithm}/config.yaml"

# Update dockerfile path (line 246)
# FROM:
dockerfile_path = PKG_ROOT/f"build/dockerfiles/{interface.capitalize()}.Dockerfile"
# TO: 
dockerfile_path = PROJ_ROOT / f"interfaces/dockerfiles/{interface.capitalize()}.Dockerfile"

# Update Docker build context (line 257)
# FROM:
"src/bilayers/build"
# TO:
str(PROJ_ROOT / "interfaces")

# Remove session.cd calls from test_parse and test_generate (lines 316, 326)
```

#### 4.2: Update Docker Templates
**Update interfaces/dockerfiles/Gradio.Dockerfile**:
```dockerfile
# Line 23: Update ADD path
# FROM:
ADD parse/generated_folders/$FOLDER_NAME/app.py /bilayers/
# TO:
ADD generated_folders/$FOLDER_NAME/app.py /bilayers/
```

**Update interfaces/dockerfiles/Jupyter.Dockerfile**:
```dockerfile  
# Line 19: Update ADD path
# FROM: 
ADD parse/generated_folders/$FOLDER_NAME/generated_notebook.ipynb /bilayers/
# TO:
ADD generated_folders/$FOLDER_NAME/generated_notebook.ipynb /bilayers/
```

#### 4.3: Update Shell Scripts
**Update scripts/build_docker.sh**:
- Path references should continue to work since PKG_ROOT still resolves correctly
- Verify algorithm paths resolve to new location

**Update scripts/validate.sh** (if exists):
```bash
# Update algorithm directory reference  
# FROM:
CONFIG_DIR="$PKG_ROOT/algorithms/${ALGORITHM}"
# TO:
CONFIG_DIR="$(dirname "$PKG_ROOT")/algorithms/${ALGORITHM}" 
```

### Phase 5: Update Tests

#### 5.1: Update CLI Tests (moved to tests/cli/)
**Update all test files in tests/cli/**: 
```python
# Update imports in test_*.py files
# FROM:
from bilayers.build.parse.parse import parse_config
from bilayers_cli.cli_generator import main  
# TO:
from bilayers.parse import parse_config
from bilayers.cli.cli_generator import main
```

#### 5.2: Update Core Tests  
**Update tests in tests/** that reference algorithm paths:
```python
# FROM:
bilayers.package_path() / "algorithms/instanseg_inference/config.yaml"
# TO:
bilayers.project_path() / "algorithms/instanseg_inference/config.yaml"
```

### Phase 6: Update src/bilayers/__init__.py
**Enhance helper functions**:
```python
from pathlib import Path

def package_path():
    """
    Returns an absolute path to the bilayers package (this one)
        /absolute/path/to/bilayers/src/bilayers/
    """
    return Path(__path__[0])

def project_path():
    """  
    Returns an absolute path to the project dir hosting the bilayers package
        /absolute/path/to/bilayers/
    """
    return (package_path() / '../..').resolve()

# Import main modules for easier access
from . import parse, generate
from .cli import cli

__all__ = ["package_path", "project_path", "parse", "generate", "cli"]
```

### Phase 7: Add Module Entry Points
**Make parse.py and generate.py executable as modules**:

**Add to src/bilayers/parse.py**:
```python
# Add at the end
if __name__ == "__main__":
    main()
```

**Add to src/bilayers/generate.py**:
```python  
# Add at the end
if __name__ == "__main__":
    main()
```

## Testing and Validation Plan

### Phase 8: Comprehensive Testing

#### 8.1: Basic Import Testing
```bash
# Test basic imports work
python -c "import bilayers; print('✓ bilayers imports')"
python -c "from bilayers import parse, generate, cli; print('✓ modules import')" 
python -c "from bilayers.parse import parse_config; print('✓ parse_config imports')"
python -c "from bilayers.cli import cli; print('✓ CLI imports')"
```

#### 8.2: CLI Testing
```bash
# Test CLI entry point
bilayers_cli --help
bilayers_cli --version

# Test with sample config
bilayers_cli algorithms/classical_segmentation/config.yaml
```

#### 8.3: Nox Session Testing  
```bash
# Test all nox sessions
nox -s run_parse -- algorithms/classical_segmentation/config.yaml
nox -s run_generate -- algorithms/classical_segmentation/config.yaml
nox -s build_algorithm -- classical_segmentation
nox -s build_interface -- gradio classical_segmentation
nox -s lint
nox -s format
```

#### 8.4: Docker Build Testing
```bash
# Test Docker builds still work
./scripts/build_docker.sh --algorithm classical_segmentation --
