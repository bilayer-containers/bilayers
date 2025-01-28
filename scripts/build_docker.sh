#!/bin/bash

# Exit on error
set -e

# List of algorithms and interfaces
# ALGORITHM_NAMES=("classical_segmentation" "cellpose_inference" "instanseg_inference")
ALGORITHM_NAMES=("cellpose_inference")
INTERFACE_NAMES=("gradio") 

# Build the Docker images for each algorithm and interface
for ALGORITHM_NAME in "${ALGORITHM_NAMES[@]}";
    do
    for INTERFACE_NAME in "${INTERFACE_NAMES[@]}";
        do
        echo "Processing Algorithm: $ALGORITHM_NAME, Interface: $INTERFACE_NAME"

        # Running the parse script by giving actual config_path
        CONFIG_PATH="../../../src/algorithms/${ALGORITHM_NAME}/config.yaml"
        nox -s run_parse -- $CONFIG_PATH

        # Running the generate file 
        CONFIG_PATH="../../../src/algorithms/${ALGORITHM_NAME}/config.yaml"
        nox -s run_generate -- $CONFIG_PATH

        # Building the Algorithm Docker image
        nox -s build_algorithm -- $ALGORITHM_NAME

        # Building the Interface Docker image
        nox -s build_interface -- $INTERFACE_NAME $ALGORITHM_NAME

        # Installing the Graadio interface
        nox -s install_gradio
    done
done
