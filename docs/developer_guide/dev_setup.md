---
title: Local Setup (pixi)
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

All Bilayers repos use **[pixi](https://pixi.sh)** for environment management — not
`pip`/`venv` directly. This page gets you from a fresh clone to running the pipeline
and tests locally.

## Clone the repositories

Bilayers is four sibling repos. For orchestrator work you mainly need `bilayers`, but
to test changes to a sibling you'll want it checked out next to `bilayers`:

```bash
git clone https://github.com/bilayer-containers/bilayers.git
git clone https://github.com/bilayer-containers/bilayers-schema.git
git clone https://github.com/bilayer-containers/bilayers-targets.git
git clone https://github.com/bilayer-containers/bilayers-algorithms.git
```

Keep them as siblings in the same parent folder.

## Environments

In `bilayers/` the two relevant pixi environments are:

- **`dev`** — general development; uses **Podman** (`DOCKER_CMD=podman`).
- **`dockerdev`** — same, but uses **Docker** (`DOCKER_CMD=docker`).

Run anything inside an environment with `pixi run -e <env> …` (run from `bilayers/`):

```bash
pixi run -e dev bilayers_cli generate <config.yaml>
pixi run -e dev nox -s test_pytest
pixi run -e dockerdev nox -s build_algorithm -- cellpose_inference
```

## Testing a change to a sibling repo (pixi-native)

By default the siblings are installed from git (at the commits in `pixi.lock`), so editing your local checkout
has **no effect** on what the orchestrator runs until you point the environment at it.
Do this the pixi-native way — **not** with a direct `pip install -e`/`uv pip install`,
which can shadow the package and cause confusing "why aren't my edits showing up"
issues.

In `bilayers/pyproject.toml`, temporarily set the sibling to a local path dependency:

```toml
[tool.pixi.pypi-dependencies]
bilayers-schema = { path = "../bilayers-schema", editable = true }
```

then re-install and run:

```bash
pixi install -e dev
pixi run -e dev nox -s test_pytest
```

When you're done, revert `pyproject.toml` and `pixi.lock` (`git checkout -- pyproject.toml pixi.lock`)
and run `pixi install -e dev` again to restore the git dependencies.

## Common commands

```bash
# CLI (inside a pixi env, e.g. `pixi run -e dev bilayers_cli ...`)
bilayers_cli parse <config.yaml>
bilayers_cli generate <config.yaml>            # all interfaces -> dist/
bilayers_cli generate <config.yaml> -i gradio  # one interface
bilayers_cli generate <config.yaml> --cli      # print the CLI command only
bilayers_cli validate <config.yaml>            # LinkML validation

# nox sessions (from bilayers/, inside a pixi env)
nox -s test_pytest                             # full pytest suite
nox -s lint                                    # ruff check
nox -s format                                  # ruff format
```

## A note on the lockfile

CI installs with `locked: true`, so `pixi.lock` decides exactly which sibling commits
are tested. If you change dependencies in `pyproject.toml`, `pixi` rewrites
`pixi.lock` — commit both together. To move the siblings to their latest `main`, run
`pixi update` and commit the lockfile. See
[Versioning & Reproducibility](../versioning/versioning.md) for the reasoning.
