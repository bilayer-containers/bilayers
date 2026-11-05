---
title: Add a New Interface
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Interfaces (and plugins) live in
[`bilayers-targets`](https://github.com/bilayer-containers/bilayers-targets). A new
interface is a small package that renders a Jinja2 template from the `InterfaceInput`
dict it's handed.

## Steps

1. Add a package under `src/bilayers_targets/interfaces/<name>/` (or `plugins/<name>/`)
   containing:
   - `generate.py` exposing `generate(interface_input)`
   - a `*.j2` Jinja2 template
   - a `<Name>.Dockerfile`, named after the interface with its first letter capitalized
     (e.g. `Gradio.Dockerfile`): `nox -s build_interface` looks it up by that name
2. Register it in `registry.py` by adding `"<name>": "bilayers_targets.interfaces.<name>.generate"`
   to `_INTERFACE_MODULES`. If importing the module raises `ModuleNotFoundError` (an optional
   dependency is missing), the registry skips it, so `bilayers_cli` just won't list it.
3. Add the optional-dependency extra in `bilayers-targets/pyproject.toml`, and the matching
   extra in `bilayers/pyproject.toml` so the orchestrator installs it.
4. Add a test in `bilayers-targets/tests/test_targets.py`. In `bilayers`, add the new output
   file to `expected_outputs` in `tests/regression/test_generate_regression.py` and commit its
   golden copy (see [Developer Testing](../testing/developer_testing.md)).

## The one hard rule

Generators must be **standalone**. They may **not** import `bilayers.parse` or
`bilayers.generate`, and must not import `project_path` from `bilayers`. Everything the
generator needs arrives in the plain `InterfaceInput` dict. That's what lets
`bilayers-targets` be released independently.

The orchestrator's pre-commit runs `scripts/check_forbidden_interface_imports.py` for
this, but the script still looks for generators at their old location inside `bilayers`,
so it currently checks nothing. Until it's pointed at `bilayers-targets`, reviewers need
to check this by hand.

## Keep command-building consistent

All interfaces build the tool's command from the same `cli_sequence`. Put shared
command-building logic in one place and reuse it across templates rather than
re-implementing per interface — divergent copies drift and produce subtly different
commands.

## Learn from an existing generator

[Inside bilayers-targets](../architecture/targets.md) walks through how the existing
generators are put together: the registry, the steps every `generate()` follows, and
how each target runs the tool. The Gradio generator is the simplest one to copy from.
