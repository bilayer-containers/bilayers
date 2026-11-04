---
title: FAQ
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

## General

**What is Bilayers?**
An open-source specification that describes a containerized tool's inputs, outputs, and
parameters once, and generates no-terminal-required interfaces (Gradio, Jupyter,
Streamlit, CellProfiler plugin) from that single description. See
[Home](../standard/WhatIsBilayers.md).

**Do I need to code to use a Bilayers tool?**
No. Pull the published Docker image and use the generated UI. See the
[User Guide](../user_guide/user_guide.md).

## Configs

**Why isn't my parameter showing up on the command line?**
It's probably under `display_only`, which is shown in the UI but never passed to the
CLI. Move anything the tool needs into `inputs` or `parameters`. See
[Core Data Flow](../architecture/data_flow.md).

**My tool produced no output — why?**
Common causes: inputs mounted to the wrong container path, or a "save output" option
not enabled. See [User Testing](../testing/user_testing.md).

## Development

**Why is Bilayers four repositories?**
To version and test the schema, generators, algorithms, and orchestrator
independently. See [How Bilayers is Organized](../architecture/overview.md).

**I edited a sibling repo but the orchestrator doesn't see my change.**
The siblings are installed from git at the commit recorded in `pixi.lock`, not from
your checkout. Point the environment at your local checkout (pixi path dependency) —
see [Local Setup](../developer_guide/dev_setup.md).

**CI is testing an older version of a sibling repo. Why?**
CI installs with `locked: true`, so it uses the sibling commits recorded in `pixi.lock`.
Run `pixi update` and commit the lockfile to move them forward. See
[Versioning & Reproducibility](../versioning/versioning.md).

**I opened a Gradio/Jupyter/Streamlit image but the page won't load.**
Publish the container's port with `-p`: Gradio and Jupyter listen on `7878`, Streamlit
on `8501`. See [Run a Bilayers Image](../tool_user/steps_to_run.md).

:::{note}
Add real user questions here as they come up in issues/discussions.
:::
