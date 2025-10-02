## Bilayers CLI

A tool for generating executable CLI commands from Bilayers specification files

## Overview

Bilayers CLI is a tool designed to parse Bilayers specification files and generate executable CLI commands. It simplifies the process of constructing command-line arguments based on a Bilayers spec file, ensuring consistency and reproducibility.

## Features

- Generates structured CLI commands
- Works as both a CLI tool and a Python library
- Outputs the generated CLI command as a string (CLI usage) or as a list (Library usage)

## Installation (Once it's published on PyPI)

### Using pip
```
pip install bilayers_cli
```

### Using Pixi (if managing dependencies via Pixi)
```
pixi add --pypi bilayers_cli
```

## Usage

### CLI Usage
Once installed, you can generate CLI commands using:
```
bilayers_cli path/to/config.yaml
```
Example:
```
bilayers_cli src/algorithms/instanseg_inference/config.yaml
```

will output the structured CLI command as a string:
```
"python /instanseg/instanseg/scripts/inference.py --image_path input_images --model_folder brightfield_nuclei --device cpu --tile_size 512 --batch_size 1"
```

### Library Usage
If you want to use Bilayers CLI as a library in your Python projects:
```
from bilayers.build.parse.parse import parse_config
from bilayers_cli.cli_generator import main

config = parse_config("path/to/config.yaml")
cli_command = main(config, return_as_string=True)
print(cli_command)  # Outputs the CLI command
```

## Development & Contribution

#### Setting Up Locally

Clone the repository and install dependencies using Pixi:
```
git clone https://github.com/bilayer-containers/bilayers.git
cd src/bilayers_cli
pixi install
```

Checking Code Quality
```
pixi run ruff check
pixi run pyright
```

Running Tests
```
pixi run pytest
```