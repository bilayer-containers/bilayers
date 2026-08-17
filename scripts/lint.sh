#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_ROOT="$("$SCRIPT_DIR"/pkg_path.sh)"
#PROJ_ROOT="$(cd "$PKG_ROOT/../.." && pwd)"

cd "$SCRIPT_DIR" || exit

# $1 optionally overrides the schema file path (defaults to schema_path.sh's output)
SCHEMA_FILE=${1:-"$("$SCRIPT_DIR"/schema_path.sh)"}

echo "Linting the schema: $SCHEMA_FILE"

if linkml-lint "$SCHEMA_FILE"; then
    echo "Schema linting successful."
else
    echo "Schema linting failed."
    exit 1
fi
