Based on my comprehensive analysis of the codebase, here's a detailed research report on the refactoring requirements:

# Bilayers Refactoring Analysis Report

## Current Structure vs. Target Structure

### Current Structure:
```
src/
├── bilayers/
│   ├── __init__.py
│   ├── algorithms/          # → TO MOVE to algorithms/
│   └── build/
│       ├── dockerfiles/     # → TO MOVE to interfaces/dockerfiles/
│       └── parse/
│           ├── parse.py     # → TO MOVE to src/bilayers/parse.py
│           ├── generate.py  # → TO MOVE to src/bilayers/generate.py
│           └── *.py.j2      # → TO MOVE to interfaces/templates/
└── bilayers_cli/
    ├── bilayers_cli/
    │   ├── cli.py           # → TO MOVE to src/bilayers/cli/cli.py
    │   └── cli_generator.py # → TO MOVE to src/bilayers/cli/cli_generator.py
    └── pyproject.toml       # → TO MERGE with top-level pyproject.toml
```

### Target Structure:
```
├── algorithms/              # MOVED from src/bilayers/algorithms/
├── interfaces/
│   ├── dockerfiles/         # MOVED from src/bilayers/build/dockerfiles/
│   └── templates/           # MOVED from src/bilayers/build/parse/*.py.j2
├── src/bilayers/
│   ├── __init__.py
│   ├── parse.py             # MOVED from src/bilayers/build/parse/parse.py
│   ├── generate.py          # MOVED from src/bilayers/build/parse/generate.py
│   └── cli/
│       ├── __init__.py      # NEW
│       ├── cli.py           # MOVED from src/bilayers_cli/bilayers_cli/cli.py
│       └── cli_generator.py # MOVED from src/bilayers_cli/bilayers_cli/cli_generator.py
└── pyproject.toml           # UNIFIED from both pyproject.toml files
```

## Critical Dependencies and Breaking Changes

### 1. **Import Dependencies (HIGH PRIORITY)**

#### **In `src/bilayers/build/parse/generate.py`:**
```python
# CURRENT - WILL BREAK:
from parse import main as parse_config  # Relative import
from parse import InputOutput, Parameter, ExecFunction, Citations

# NEEDS TO BECOME:
from bilayers.parse import main as parse_config
from bilayers.parse import InputOutput, Parameter, ExecFunction, Citations
```

#### **In `src/bilayers_cli/bilayers_cli/cli.py`:**
```python
# CURRENT - WILL BREAK:
from bilayers.build.parse.parse import parse_config
from bilayers_cli.bilayers_cli.cli_generator import main

# NEEDS TO BECOME:
from bilayers.parse import parse_config
from bilayers.cli.cli_generator import main
```

#### **In `src/bilayers_cli/bilayers_cli/cli_generator.py`:**
```python
# CURRENT - WILL BREAK:
from bilayers.build.parse.parse import Config, HiddenArgs

# NEEDS TO BECOME:
from bilayers.parse import Config, HiddenArgs
```

### 2. **Hardcoded Path References (HIGH PRIORITY)**

#### **In `noxfile.py`:**
```python
# CURRENT - WILL BREAK:
session.cd(PKG_ROOT/"build/parse")                    # Lines 104, 120, 316, 326
algorithm_path = PKG_ROOT / f"algorithms/{algorithm}" # Line 147
config_file_path = PKG_ROOT/f"algorithms/{algorithm}/config.yaml" # Line 170
dockerfile_path = PKG_ROOT/f"build/dockerfiles/{interface.capitalize()}.Dockerfile" # Line 246
"src/bilayers/build"                                  # Line 257

# NEEDS TO BECOME:
# No session.cd needed - run directly from project root
algorithm_path = PROJ_ROOT / f"algorithms/{algorithm}"
config_file_path = PROJ_ROOT / f"algorithms/{algorithm}/config.yaml"
dockerfile_path = PROJ_ROOT / f"interfaces/dockerfiles/{interface.capitalize()}.Dockerfile"
"interfaces"  # Docker build context
```

#### **In `src/bilayers/build/parse/parse.py`:**
```python
# CURRENT - WILL BREAK:
config_path = bilayers.package_path() / "algorithms/classical_segmentation/config.yaml"  # Line 91
config_path = Path("../../../src/bilayers/algorithms/classical_segmentation/config.yaml") # Line 93

# NEEDS TO BECOME:
config_path = bilayers.project_path() / "algorithms/classical_segmentation/config.yaml"
config_path = Path("algorithms/classical_segmentation/config.yaml")  # From project root
```

#### **In `scripts/build_docker.sh`:**
```bash
# CURRENT - WILL BREAK:
CONFIG_PATH="${PKG_ROOT}/algorithms/${ALGO}/config.yaml"  # Line 55

# NEEDS TO BECOME:
CONFIG_PATH="${PKG_ROOT}/algorithms/${ALGO}/config.yaml"  # Same, but PKG_ROOT now points to project root
```

#### **In Docker Templates:**
```dockerfile
# CURRENT - WILL BREAK:
ADD parse/generated_folders/$FOLDER_NAME/app.py /bilayers/
ADD parse/generated_folders/$FOLDER_NAME/generated_notebook.ipynb /bilayers/

# NEEDS TO BECOME:
ADD generated_folders/$FOLDER_NAME/app.py /bilayers/
ADD generated_folders/$FOLDER_NAME/generated_notebook.ipynb /bilayers/
```

### 3. **Template File References (HIGH PRIORITY)**

#### **In `src/bilayers/build/parse/generate.py`:**
```python
# CURRENT - WILL BREAK:
"jupyter_final_validation_template.py.j2"  # Line 188
"jupyter_shell_command_template.py.j2"     # Line 201
"gradio_template.py.j2"                     # Line 234
"jupyter_template.py.j2"                    # Line 252

# NEEDS TO BECOME:
# Update template loading to use absolute paths from interfaces/templates/
template_dir = bilayers.project_path() / "interfaces/templates"
env = Environment(loader=FileSystemLoader(searchpath=template_dir), ...)
```

### 4. **CLI Entry Point (MEDIUM PRIORITY)**

#### **In `src/bilayers_cli/pyproject.toml`:**
```toml
# CURRENT - WILL BREAK:
[project.scripts]
bilayers_cli = "bilayers_cli.cli:cli"

# NEEDS TO BECOME (in unified pyproject.toml):
[project.scripts]
bilayers_cli = "bilayers.cli.cli:cli"
```

### 5. **Package Configuration Unification (HIGH PRIORITY)**

#### **Current Separate Configurations:**
- **Top-level `pyproject.toml`**: bilayers package, line-length=160, ruff config
- **`src/bilayers_cli/pyproject.toml`**: bilayers_cli package, line-length=100, different dependencies

#### **Unified Configuration Needed:**
```toml
[project]
name = "bilayers"
version = "0.1.0"
description = "Specifications and automated interfaces for wrapped tools"
dependencies = [
    "nox>=2024.4.15,<2025",
    "pyyaml>=6.0.1,<7",
]

[project.scripts]
bilayers_cli = "bilayers.cli.cli:cli"

[project.optional-dependencies]
dev = [
    "numpy", "scipy", "scikit-image", "jinja2", "nbformat", 
    "ipython", "ipywidgets", "gradio", "pytest", "ruff", "pyright"
]

[tool.ruff]
line-length = 160  # Keep the more permissive setting
```

## Refactoring Strategy and Order

### **Phase 1: Preparation**
1. **Create new directory structure** (algorithms/, interfaces/)
2. **Create new CLI module structure** (src/bilayers/cli/)
3. **Unify pyproject.toml** configurations

### **Phase 2: Move Files**
1. **Move algorithms**: `src/bilayers/algorithms/` → `algorithms/`
2. **Move dockerfiles**: `src/bilayers/build/dockerfiles/` → `interfaces/dockerfiles/`
3. **Move templates**: `src/bilayers/build/parse/*.py.j2` → `interfaces/templates/`
4. **Move parse modules**: 
   - `src/bilayers/build/parse/parse.py` → `src/bilayers/parse.py`
   - `src/bilayers/build/parse/generate.py` → `src/bilayers/generate.py`
5. **Move CLI modules**:
   - `src/bilayers_cli/bilayers_cli/cli.py` → `src/bilayers/cli/cli.py`
   - `src/bilayers_cli/bilayers_cli/cli_generator.py` → `src/bilayers/cli/cli_generator.py`

### **Phase 3: Update References**
1. **Update all import statements** in moved files
2. **Update noxfile.py** path references and session logic
3. **Update Docker template file paths**
4. **Update shell script paths**
5. **Update template loading logic** in generate.py
6. **Update fallback paths** in parse.py

### **Phase 4: Testing and Validation**
1. **Test all nox sessions** work with new structure
2. **Test CLI functionality** with new entry point
3. **Test Docker builds** with new paths
4. **Validate all imports** resolve correctly

## Key Risks and Mitigation

### **High Risk Areas:**
1. **Nox sessions** - Extensive path changes needed
2. **Docker builds** - File path references in Dockerfiles and build contexts
3. **Template loading** - Jinja2 template discovery needs updating
4. **CLI entry point** - Package script configuration changes

### **Mitigation Strategies:**
1. **Incremental testing** - Test each phase before proceeding
2. **Backup current working state** before starting
3. **Update bilayers.__init__.py** helper functions if needed
4. **Consider adding compatibility shims** during transition

## Files Requiring Updates

### **Critical Updates (Must Change):**
- `noxfile.py` (extensive path updates)
- `src/bilayers/build/parse/generate.py` (imports + template paths)
- `src/bilayers/build/parse/parse.py` (fallback paths)
- `src/bilayers_cli/bilayers_cli/cli.py` (imports)
- `src/bilayers_cli/bilayers_cli/cli_generator.py` (imports)
- `src/bilayers/build/dockerfiles/*.Dockerfile` (file paths)
- `scripts/build_docker.sh` (algorithm paths)
- `scripts/validate.sh` (algorithm paths)
- Top-level `pyproject.toml` (unification)

### **Test Updates:**
- All test files in `src/bilayers_cli/tests/` (import paths)
- All test files in `tests/` (path references)

### **Documentation Updates:**
- Any documentation referencing old paths
- CI/CD workflows if they reference specific paths

This refactoring will significantly simplify the project structure and create a unified bilayers library with integrated CLI functionality, but requires careful coordination of all path dependencies.
