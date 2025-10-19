#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_ROOT="$("$SCRIPT_DIR"/pkg_path.sh)"
#PROJ_ROOT="$(cd "$PKG_ROOT/../.." && pwd)"

cd "$SCRIPT_DIR" || exit

SCHEMA_FILE=${1:-"$PKG_ROOT/schema.yaml"}

echo "Linting the schema: $SCHEMA_FILE"

if linkml-lint "$SCHEMA_FILE"; then
    echo "Schema linting successful."
else
    echo "Schema linting failed."
    exit 1
fi
