#!/usr/bin/env bash
set -euo pipefail

# Ensure we're inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Not inside a git repository, skipping pre-commit installation..."
    exit 0
fi

# Ensure pre-commit is available
if ! command -v pre-commit >/dev/null 2>&1; then
    echo "pre-commit is not available in this environment, skipping hook installation..."
    exit 0
fi

# Find git hooks directory
# https://stackoverflow.com/questions/14073053/find-path-to-git-hooks-directory-on-the-shell
hooks_dir="$(git config --get core.hooksPath 2>/dev/null || git rev-parse --git-path hooks)"

# Install pre-commit hook only if not already present
if [ ! -f "$hooks_dir/pre-commit" ]; then
    echo "Installing pre-commit hooks..."
    pre-commit validate-config
    pre-commit install
    echo "Pre-commit hooks installed!"
else
    echo "Pre-commit hooks already installed. Skipping..."
fi