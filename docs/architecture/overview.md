---
title: How Bilayers is Organized
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers is not a single repository — it is **four repositories** that work together.
Splitting them keeps each concern independently versioned, tested, and installable.

## The four repositories

- **[`bilayers`](https://github.com/bilayer-containers/bilayers)** — the **orchestrator**.
  Provides the `bilayers_cli` entry point (`parse`, `generate`, `validate`) and the
  CI/build glue (nox sessions, Docker build scripts, these docs). This is where a
  single config becomes a set of runnable interfaces.
- **[`bilayers-schema`](https://github.com/bilayer-containers/bilayers-schema)** — the
  **LinkML schema** (`schema.yaml`) every config is validated against, plus the
  generated Python `TypedDict` types (`Config`, `Input`, `Output`, `Parameter`,
  `DockerImage`, `ExecFunction`, …) that everything else imports. The schema is the
  source of truth; the types are a hand-maintained mirror kept in sync by a drift test.
- **[`bilayers-targets`](https://github.com/bilayer-containers/bilayers-targets)** — the
  interface/plugin **generators**: `gradio`, `jupyter`, `streamlit`, and the
  `cellprofiler_plugin`. Each is a `generate.py` + a Jinja2 template. They are
  **standalone** — they never import the orchestrator; they receive everything through
  a plain `InterfaceInput` dict.
- **[`bilayers-algorithms`](https://github.com/bilayer-containers/bilayers-algorithms)** —
  the wrapped image-analysis tools (e.g. `cellpose_inference`, `stardist_inference`,
  `instanseg_inference`, `classical_segmentation`, `gaussian_smoothing`). Each is a
  folder with a `config.yaml` (the Bilayers spec for that tool) and usually a
  `Dockerfile`.

## How they depend on each other

```{mermaid}
flowchart TB
    B["bilayers<br/>(orchestrator)"]
    T["bilayers-targets<br/>(generators)"]
    A["bilayers-algorithms<br/>(configs + Dockerfiles)"]
    S["bilayers-schema<br/>(schema.yaml + types)"]
    B --> T
    B --> A
    B --> S
    T --> S
    A --> S
```
:::{admonition} TODO
:class: warning
Replace the above one with Nodar's architecture flowchart
:::


`bilayers` depends on all three; `bilayers-targets` and `bilayers-algorithms` depend
only on `bilayers-schema`. The siblings are installed from git (their `main`
branch, at the commits recorded in `pixi.lock`), not from local checkouts — see
[Versioning & Reproducibility](../versioning/versioning.md).

## Assets come from the installed packages, not from this repo

A consequence of the split worth internalizing: the orchestrator discovers algorithms,
interfaces, and the schema **from the installed packages** — not from files inside the
`bilayers` repo. For example, the schema path resolves from the installed
`bilayers_schema` package, and algorithm configs are read from the installed
`bilayers_algorithms` package. When you change a sibling and want to test it through
`bilayers`, point the environment at your local checkout (see
[Local Setup](../developer_guide/dev_setup.md)).

## What the system does

A tool's command-line behavior is described once in a Bilayers `config.yaml` (inputs,
outputs, parameters, exec function, docker image, citations). The pipeline turns that
single spec into multiple no-terminal-required UIs — a Gradio app, a Jupyter notebook,
a Streamlit app, and a CellProfiler plugin — each baked into a Docker image. The same
container runs on a laptop, an HPC cluster, or the cloud, eliminating version drift
between prototype and production.

See [Core Data Flow](data_flow.md) for exactly what happens when you generate.
