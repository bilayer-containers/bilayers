#!/usr/bin/env bash

# Finds the absolute path of the bilayers package
# NOTE: does not contain trailing "/"
# e.g. "/path/to/bilayers-repo/src/bilayers"
#
# When used by another script in this dir, can be used like so:
#     SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
#     PKG_ROOT="$("$SCRIPT_DIR"/pkg_path.sh)"
#     PROJ_ROOT="$(cd "$PKG_ROOT/../.." && pwd)"

set -e

# if python is available
if command -v python >/dev/null 2>&1; then
    # prefer bilayers package path, if available
  PKG_ROOT=$(python -c "import bilayers; print(bilayers.__path__[0])" 2>/dev/null || \
             python -c "import pathlib, sys; print(pathlib.Path(sys.argv[1]).resolve().parent.parent)" "$0")
else
  # more hacky, but more portable than using `realpath`
  PKG_ROOT=$(cd "$(dirname "$0")/../src/bilayers" && pwd)
fi

echo "$PKG_ROOT"
