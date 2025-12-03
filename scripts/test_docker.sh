#!/bin/bash

# Exit on error
set -e

# TODO: move this to either tests/ or scripts/
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_ROOT="$("$SCRIPT_DIR"/pkg_path.sh)"
PROJ_ROOT="$(cd "$PKG_ROOT/../.." && pwd)"

# List of algorithms and interfaces
ALGORITHM_NAMES=("test_algorithm")
INTERFACE_NAMES=("gradio" "jupyter" "cellprofiler_plugin")

# Build the Docker images for each algorithm and interface
for ALGORITHM_NAME in "${ALGORITHM_NAMES[@]}";
    do
    for INTERFACE_NAME in "${INTERFACE_NAMES[@]}";
        do
        echo "Processing Algorithm: $ALGORITHM_NAME, Interface: $INTERFACE_NAME"

        # Running the parse script by giving actual config_path
        CONFIG_PATH="$PROJ_ROOT/tests/test_algorithm/correct_validation_config.yaml"
        nox -s test_parse -- "$CONFIG_PATH"

        # Running the generate file 
        CONFIG_PATH="$PROJ_ROOT/tests/test_algorithm/correct_validation_config.yaml"
        nox -s test_generate -- "$CONFIG_PATH"
    done
done
