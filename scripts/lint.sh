#!/bin/bash
cd "$(dirname "$0")"
SCHEMA_FILE=${1:-"../schema/validate_schema.yaml"}

echo "Linting the schema: $SCHEMA_FILE"
linkml-lint "$SCHEMA_FILE"

if [ $? -eq 0 ]; then
    echo "Schema linting successful."
else
    echo "Schema linting failed."
    exit 1
fi
