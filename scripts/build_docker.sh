#!/usr/bin/env bash

# Continue building remaining algorithm/interface combinations even if one fails
# Fail the workflow at the end if any build failures occurred


if ! ALGO_PKG_PATH=$(python -c "import bilayers_algorithms; import os; print(os.path.dirname(bilayers_algorithms.__file__))"); then
  echo "Could not locate installed bilayers_algorithms package."
  exit 1
fi
# List of algorithms and interfaces
ALGORITHM_NAMES=()
INTERFACE_NAMES=()
BUMP_TYPE="minor"
# Collect failures and report them after all build combinations have been attempted
FAILURES=()

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

# Attempt every algorithm/interface combination independently
for ALGO in "${ALGORITHM_NAMES[@]}"; do
  for IFACE in "${INTERFACE_NAMES[@]}"; do
    echo "Building Algorithm: $ALGO, Interface: $IFACE"

    CONFIG_PATH="${ALGO_PKG_PATH}/${ALGO}/config.yaml"
    if ! nox -s run_parse -- "$CONFIG_PATH"; then
      FAILURES+=("$ALGO:$IFACE:run_parse")
      continue
    fi

    if ! nox -s run_generate_all -- "$CONFIG_PATH"; then
      FAILURES+=("$ALGO:$IFACE:run_generate_all")
      continue
    fi

    if ! nox -s build_algorithm -- "$ALGO"; then
      FAILURES+=("$ALGO:$IFACE:build_algorithm")
      continue
    fi

    if ! nox -s build_interface -- "$IFACE" "$BUMP_TYPE"; then
      FAILURES+=("$ALGO:$IFACE:build_interface")
      continue
    fi

    if [[ "$IFACE" == "gradio" ]]; then
      if ! nox -s install_gradio; then
        FAILURES+=("$ALGO:$IFACE:install_gradio")
        continue
      fi

    elif [[ "$IFACE" == "streamlit" ]]; then
      if ! nox -s install_streamlit; then
        FAILURES+=("$ALGO:$IFACE:install_streamlit")
        continue
      fi
    fi
  done
done

if [[ ${#FAILURES[@]} -gt 0 ]]; then
  echo "Some builds failed:"
  printf ' - %s\n' "${FAILURES[@]}"
  exit 1
fi

echo "All builds completed successfully!"