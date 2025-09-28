#!/bin/bash

# Exit on error
set -e

# List of algorithms and interfaces
ALGORITHM_NAMES=()
INTERFACE_NAMES=()

# Parse cli arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --algorithm)
      shift
      while [[ "$#" -gt 0 && ! "$1" =~ ^-- ]]; do
        ALGORITHM_NAMES+=("$1")
        shift
      done
      ;;
    --interface)
      shift
      while [[ "$#" -gt 0 && ! "$1" =~ ^-- ]]; do
        INTERFACE_NAMES+=("$1")
        shift
      done
      ;;
    *)
      echo "Unknown parameter: $1"; exit 1 ;;
  esac
done

# Defaults if none passed
if [[ ${#ALGORITHM_NAMES[@]} -eq 0 ]]; then
  ALGORITHM_NAMES=("classical_segmentation" "cellpose_inference" "instanseg_inference" "gaussian_smoothing")
fi

if [[ ${#INTERFACE_NAMES[@]} -eq 0 ]]; then
  INTERFACE_NAMES=("gradio" "jupyter")
fi

# Build loop
for ALGO in "${ALGORITHM_NAMES[@]}"; do
  for IFACE in "${INTERFACE_NAMES[@]}"; do
    echo "Building Algorithm: $ALGO, Interface: $IFACE"

    CONFIG_PATH="../../../../src/bilayers/algorithms/${ALGO}/config.yaml"
    nox -s run_parse -- "$CONFIG_PATH"
    nox -s run_generate -- "$CONFIG_PATH"
    nox -s build_algorithm -- "$ALGO"
    nox -s build_interface -- "$IFACE" "$ALGO"

    if [[ "$IFACE" == "gradio" ]]; then
      nox -s install_gradio
    fi
  done
done

# # Build the Docker images for each algorithm and interface
# for ALGORITHM_NAME in "${ALGORITHM_NAMES[@]}";
#     do
#     for INTERFACE_NAME in "${INTERFACE_NAMES[@]}";
#         do
#         echo "Processing Algorithm: $ALGORITHM_NAME, Interface: $INTERFACE_NAME"

#         # Running the parse script by giving actual config_path
#         CONFIG_PATH="../../../../src/bilayers/algorithms/${ALGORITHM_NAME}/config.yaml"
#         nox -s run_parse -- $CONFIG_PATH

#         # Running the generate file
#         CONFIG_PATH="../../../../src/bilayers/algorithms/${ALGORITHM_NAME}/config.yaml"
#         nox -s run_generate -- $CONFIG_PATH

#         # Building the Algorithm Docker image
#         nox -s build_algorithm -- $ALGORITHM_NAME

#         # Building the Interface Docker image
#         nox -s build_interface -- $INTERFACE_NAME $ALGORITHM_NAME

#         # Installing the Graadio interface
#         nox -s install_gradio
#     done
# done
