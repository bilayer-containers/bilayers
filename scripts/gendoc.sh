#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_ROOT="$("$SCRIPT_DIR"/pkg_path.sh)"
PROJ_ROOT="$(cd "$PKG_ROOT/../.." && pwd)"

SCHEMA_FILE="${PROJ_ROOT}/tests/test_config/validate_schema.yaml"
DOCS_DIR="${PROJ_ROOT}/docs/developer"
# DOCS_OUTPUT = "${DOCS_DIR}/schema_docs.md"

# Check if LinkML is installed
if ! command -v gen-doc &> /dev/null
then
    echo "LinkML is not installed. Please install it using 'pip install linkml'."
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p "${DOCS_DIR}"

# Generate the documentation
linkml generate doc --format markdown --directory "${DOCS_DIR}" "${SCHEMA_FILE}"

echo "Documentation generated successfully in ${DOCS_DIR}"
