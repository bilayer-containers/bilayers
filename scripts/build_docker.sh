#!/usr/bin/env bash

# Exit on error
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_ROOT="$("$SCRIPT_DIR"/pkg_path.sh)"
PROJ_ROOT="$(cd "$PKG_ROOT/../.." && pwd)"

# List of algorithms and interfaces
ALGORITHM_NAMES=()
INTERFACE_NAMES=()
BUMP_TYPE="minor"

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
    --bump_type)
      shift
      BUMP_TYPE="$1"
      shift
      ;;
    *)
      echo "Unknown parameter: $1"; exit 1 ;;
  esac
done

# Defaults if none passed
if [[ ${#ALGORITHM_NAMES[@]} -eq 0 ]]; then
  ALGORITHM_NAMES=("classical_segmentation" "cellpose_inference" "instanseg_inference" "gaussian_smoothing" "stardist_inference")
fi

if [[ ${#INTERFACE_NAMES[@]} -eq 0 ]]; then
  INTERFACE_NAMES=("gradio" "jupyter" "streamlit")
fi

# Build loop
for ALGO in "${ALGORITHM_NAMES[@]}"; do
  for IFACE in "${INTERFACE_NAMES[@]}"; do
    echo "Building Algorithm: $ALGO, Interface: $IFACE"

    CONFIG_PATH="${PROJ_ROOT}/algorithms/${ALGO}/config.yaml"
    nox -s run_parse -- "$CONFIG_PATH"
    nox -s run_generate_all -- "$CONFIG_PATH"
    nox -s build_algorithm -- "$ALGO"
    nox -s build_interface -- "$IFACE" "$BUMP_TYPE"

    if [[ "$IFACE" == "gradio" ]]; then
      nox -s install_gradio
    elif [[ "$IFACE" == "streamlit" ]]; then
      nox -s install_streamlit
    fi
  done
done
