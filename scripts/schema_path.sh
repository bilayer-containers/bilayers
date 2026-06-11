#!/usr/bin/env bash

SCHEMA_FILE="$("$SCRIPT_DIR"/schema_path.sh)"
echo "Validating algorithm configs against installed schema: $SCHEMA_FILE"