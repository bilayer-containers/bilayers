---
title: Core Data Flow
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

This page traces what happens inside the orchestrator (`bilayers`) when you turn a
config into interfaces.

## The pipeline

1. **Parse** — `parse.py:parse_config` loads the YAML and normalizes the list-valued
   sections (`inputs`, `outputs`, `parameters`, `display_only`, `citations`,
   `exec_function.hidden_args`) into name-keyed dictionaries. `safe_parse_config`
   applies defaults and returns the canonical tuple consumed everywhere downstream.

2. **Build the CLI sequence** — `parse.py:build_cli_sequence` merges inputs +
   parameters + hidden_args into a single ordered dict, sorted by `cli_order`
   (positives ascending → zeros → negatives). This centralizes CLI argument ordering
   so individual interface generators never re-implement it.

3. **Generate** — `generate.py` builds an `InterfaceInput` dict and hands it to a
   generator resolved through `interface_loader.py`, which wraps
   `bilayers_targets.available_ifaces`. Output is written to
   `dist/<interface>/<algorithm_folder_name>/`.

4. **Render** — each `bilayers_targets/.../generate.py` exposes `generate(interface_input)`
   and renders its Jinja2 template into the concrete interface (a Gradio `app.py`, a
   Jupyter notebook, a Streamlit app, or a CellProfiler plugin `.py`).

5. **Package** — a Docker image is built per algorithm × interface, so the same
   container runs anywhere.

## Try it yourself

```bash
# Print just the CLI command a config produces (generates nothing):
pixi run -e dev bilayers_cli generate <config.yaml> --cli

# Generate every interface into dist/:
pixi run -e dev bilayers_cli generate <config.yaml>

# Generate one interface:
pixi run -e dev bilayers_cli generate <config.yaml> -i gradio

# Validate a config against the schema:
pixi run -e dev bilayers_cli validate <config.yaml>
```

## Architectural rule (enforced by pre-commit)

Interface generators in `bilayers-targets` must be **standalone**: they may **not**
import `bilayers.parse` or `bilayers.generate`, and must not import `project_path`
from `bilayers`. They receive everything via the plain `InterfaceInput` dict. This is
enforced by `scripts/check_forbidden_interface_imports.py`, and it's what lets the
generators live in — and be released from — their own repository.

## A subtlety: `display_only` is not passed to the CLI

`build_cli_sequence` merges only inputs + parameters + hidden_args. Fields under
`display_only` are shown in the generated UI but are **never added to the command**.
So anything the tool actually needs (model choice, thresholds, the output-path field)
must live in `inputs` or `parameters` — not `display_only`. See
[The Config Model](../custom_algorithm/understanding_config.md).
