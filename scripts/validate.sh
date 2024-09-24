#!/bin/bash

cd "$(dirname "$0")"
SCHEMA_FILE=${1:-"../schema/validate_schema.yaml"}
# List of algorithms and interfaces
ALGORITHM_NAMES=("cellpose_inference" "threshold_inference") 
# INTERFACE_NAMES=("gradio" "jupyter") 

echo "Validating all config files against the schema $SCHEMA_FILE"

for ALGORITHM in "${ALGORITHM_NAMES[@]}"; do
    CONFIG_DIR="../src/Algorithms/${ALGORITHM}"
    echo "Validating all config files in $CONFIG_DIR"
    for config in "$CONFIG_DIR"/*.yaml; do
        echo "Validating $config..."
        linkml validate --schema "$SCHEMA_FILE" --target-class Container "$config" || {
            echo "Validation failed for $config"
            exit 1
        }
    done
done

echo "All config files validated successfully."
