#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR" || exit

# Prefer explicit ALGORITHMS_PATH env override, otherwise use installed package
if [ -n "$ALGORITHMS_PATH" ]; then
    ALGO_PKG_PATH="$ALGORITHMS_PATH"
else
    ALGO_PKG_PATH=$(python -c "import bilayers_algorithms; import os; print(os.path.dirname(bilayers_algorithms.__file__))")
fi

# $1 optionally overrides the schema file path (defaults to schema_path.sh's output)
SCHEMA_FILE=${1:-"$("$SCRIPT_DIR"/schema_path.sh)"}
# List of algorithms and interfaces
ALGORITHM_NAMES=("cellpose_inference" "classical_segmentation" "instanseg_inference" "stardist_inference")

echo "Validating all config files against the schema $SCHEMA_FILE"

for ALGORITHM in "${ALGORITHM_NAMES[@]}"; do
    CONFIG_DIR="${ALGO_PKG_PATH}/${ALGORITHM}"
    echo "Validating all config files in $CONFIG_DIR"

    if [ ! -d "$CONFIG_DIR" ]; then
        echo "Skipping ${CONFIG_DIR}: directory not found"
        continue
    fi

    # Enable nullglob so the glob expands to an empty list when no matches
    shopt -s nullglob
    configs=("$CONFIG_DIR"/*.yaml)
    shopt -u nullglob

    if [ ${#configs[@]} -eq 0 ]; then
        echo "No config files found in ${CONFIG_DIR}, skipping"
        continue
    fi

    for config in "${configs[@]}"; do
        echo "Validating ${config} ..."
        bilayers_cli validate "${config}" || {
            echo "Validation failed for ${config}"
            exit 1
        }
    done
done

echo "All config files validated successfully."
