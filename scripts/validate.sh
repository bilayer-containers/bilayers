#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_ROOT="$("$SCRIPT_DIR"/pkg_path.sh)"
PROJ_ROOT="$(cd "$PKG_ROOT/../.." && pwd)"

cd "$SCRIPT_DIR" || exit

SCHEMA_FILE=${1:-"$PROJ_ROOT/tests/test_config/validate_schema.yaml"}
# List of algorithms and interfaces
ALGORITHM_NAMES=("cellpose_inference" "classical_segmentation" "instanseg_inference") 

echo "Validating all config files against the schema $SCHEMA_FILE"

for ALGORITHM in "${ALGORITHM_NAMES[@]}"; do
    CONFIG_DIR="$PKG_ROOT/algorithms/${ALGORITHM}"
    echo "Validating all config files in $CONFIG_DIR"
    for config in "$CONFIG_DIR"/*.yaml; do
        echo "Validating ${config} ..."
        linkml validate --schema "$SCHEMA_FILE" --target-class SpecContainer "${config}" || {
            echo "Validation failed for ${config}"
            exit 1
        }
    done
done

echo "All config files validated successfully."
