#!/usr/bin/env bash

# Prints the absolute path to the installed bilayers_schema/schema.yaml.
# Used by lint.sh / gendoc.sh / validate.sh to locate the schema.

set -euo pipefail

python -c "import bilayers_schema, os; print(os.path.join(os.path.dirname(bilayers_schema.__file__), 'schema.yaml'))"
