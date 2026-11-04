---
title: User Guide
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

The User Guide is for people who want to **run** Bilayers tools — no coding or complex
installation required. Every algorithm × interface pair is published as a Docker image;
you spin up a container and use a friendly UI.

## Where to start

- **[Get Started](../tool_user/tool_user.md)** — the quickest path to running a
  pre-built image.
- **[Run a Bilayers Image](../tool_user/steps_to_run.md)** — mounting inputs/outputs
  and launching each interface.
- **[Catalog: Algorithms](catalog_algorithms.md)** — what tools are available.
- **[Catalog: Interfaces](catalog_interfaces.md)** — the UI options (Gradio, Jupyter,
  Streamlit, CellProfiler plugin).

## Bird's-eye view

You pick an **algorithm** (e.g. StarDist, Cellpose) and an **interface** (how you want
to interact with it), pull the matching Docker image, mount your data, and run. The
same image runs identically on a laptop, HPC, or the cloud.

:::{note}
The catalog pages are being populated from the algorithm and interface repositories.
See [issue #127](https://github.com/bilayer-containers/bilayers/issues/127) and
[#128](https://github.com/bilayer-containers/bilayers/issues/128).
:::
