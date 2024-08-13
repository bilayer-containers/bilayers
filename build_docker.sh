#!/bin/bash

# Exit on error
set -e

# List of algorithms and interfaces
ALGORITHM_NAMES=("cellpose") 
INTERFACE_NAMES=("gradio" "jupyter")

# Build the Docker images for each algorithm and interface
for ALGORITHM_NAME in "${ALGORITHM_NAMES[@]}";
    do
    for INTERFACE_NAME in "${INTERFACE_NAMES[@]}";
        do
        echo "Processing Algorithm: $ALGORITHM_NAME, Interface: $INTERFACE_NAME"

        # Running the parse script by giving actual config_path
        CONFIG_PATH="./src/Algorithm/${ALGORITHM_NAME}/config.yaml"
        nox -s run_parse -- $CONFIG_PATH

        # Running the generate file 
        nox -s run_generate

        # Building the Algorithm Docker image
        nox -s build_algorithm -- $ALGORITHM_NAME

        # Building the Interface Docker image
        nox -s build_interface -- $INTERFACE_NAME

        # Installing the Graadio interface
        nox -s install_gradio
    done
done
