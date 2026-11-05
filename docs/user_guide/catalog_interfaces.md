---
title: "Catalog: Interfaces"
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

The interfaces Bilayers can generate for any wrapped algorithm. Each lives in
[`bilayers-targets`](https://github.com/bilayer-containers/bilayers-targets) and is
exposed through the `available_ifaces` registry.

:::{note}
**This page will be auto-generated** from the interface registry
([#128](https://github.com/bilayer-containers/bilayers/issues/128)). Manual placeholder
for now.
:::

| Interface | What you get | Runs as | Best for |
| --- | --- | --- | --- |
| **Gradio** | A web app with widgets, file upload, and a zip download of the results | Docker image, port `7878` | Quick interactive use in the browser |
| **Jupyter** | A generated notebook with widgets that builds and runs the tool's command | Docker image, port `7878` | Reproducible, shareable analysis; seeing the code |
| **Streamlit** | A web app (upload → run → download) | Docker image, port `8501` | Interactive use; alternative to Gradio |
| **CellProfiler plugin** | A generated module you add to an existing CellProfiler installation | Python file; runs the algorithm's base image in Docker or Podman | Adding the tool as a step in CellProfiler pipelines |

See [Supported Interfaces](../custom_algorithm/supported_interfaces.md) for more on each.

<!--
TODO (#128): auto-generate this page. Plan:
1. Same script as #127 (scripts/build_catalog.py; draft at ../build_catalog_draft.py).
2. One row per entry in bilayers_targets.available_ifaces, so a newly registered interface appears
   automatically.
3. Derive: Interface vs Plugin (module path under interfaces/ or plugins/), description and license
   from the generator's CITATION constant, port from EXPOSE in its *.Dockerfile (no Dockerfile =
   plugin), and the file it writes by running generate() once on a real config into a temp folder.
   Name that folder "algorithm": the CellProfiler plugin derives its file name from the folder name.
4. Keep a small hand-written "Best for" map in the script; unknown interfaces get "—".
5. Gap: the CellProfiler generator has no CITATION constant, so it has no description. Add one in
   bilayers-targets, or keep a fallback in the script.
6. Run in deploy.yml before `myst build`, together with #127.
-->
