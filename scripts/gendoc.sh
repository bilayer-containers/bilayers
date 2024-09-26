#!/bin/bash

SCHEMA_FILE=schema/validate_schema.yaml
DOCS_DIR=docs/developer
# DOCS_OUTPUT = $(DOCS_DIR)/schema_docs.md

# Check if LinkML is installed
if ! command -v gen-doc &> /dev/null
then
    echo "LinkML is not installed. Please install it using 'pip install linkml'."
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p "$DOCS_DIR"

# Generate the documentation
linkml generate doc --format markdown --directory $DOCS_DIR $SCHEMA_FILE

echo "Documentation generated successfully in $DOCS_DIR"