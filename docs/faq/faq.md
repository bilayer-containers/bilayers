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
[Home](../standard/WhatIsBilayers.md), or watch the
[introduction video](../resources/talks_tutorials.md).

**Do I need to code to use a Bilayers tool?**
No. You need Docker (or Podman) installed, then you pull the published image and use the
interface in your browser. See the [User Guide](../user_guide/user_guide.md).

**Which tools are available, and which image do I pull?**
See [Catalog: Algorithms](../user_guide/catalog_algorithms.md) for the tools and their
published images, and [Run a Bilayers Image](../tool_user/steps_to_run.md) for how to
start one.

**How do I cite Bilayers?**
Use the Zenodo DOI and the citations listed in the app you used. See
[Cite Bilayers](../resources/talks_tutorials.md#cite-bilayers).

## Running a tool

**I opened a Gradio/Jupyter/Streamlit image but the page won't load.**
Publish the container's port with `-p`: Gradio and Jupyter listen on `7878`, Streamlit
on `8501`. For example, `docker run --rm -p 7878:7878 <image>`, then open
`http://localhost:7878`. See [Run a Bilayers Image](../tool_user/steps_to_run.md).

**The Jupyter notebook doesn't see my images.**
Mount your folder at the container path the config expects, usually
`-v /your/images:/bilayers/input_images`. When it works, the notebook says
**Using Mounted Directory**. See [User Testing](../testing/user_testing.md).

**My run finished but there are no output files.**
Check that your inputs arrived (uploaded, or mounted at the right path) and that any
"save" options the tool offers are switched on. The interface shows the tool's own error
message if the run failed. See [User Testing](../testing/user_testing.md).

**Gradio printed a `gradio.live` link. Is my data public?**
Gradio apps start with sharing on, so Gradio also creates a temporary public link while
the container runs. Anyone with that link can use the app. Don't share it if your images
are confidential; `http://localhost:7878` works without it.

**Do I need Docker for the CellProfiler plugin?**
Yes, Docker or Podman. The plugin is a file you add to CellProfiler, and when the module
runs it starts the algorithm's image in a container. Choose Docker or Podman in the
module's settings.

## Writing a config

**Is there a form instead of writing YAML by hand?**
Yes: the [Bilayers Config Generator](https://bilayer-containers.github.io/bilayers-config-generator/)
and the [Bilayers schema form](https://bilayers-schema.streamlit.app/). You still need to
understand the fields; see [The Config Model](../custom_algorithm/understanding_config.md).

**Why isn't my parameter showing up on the command line?**
It's probably under `display_only`, which is shown in the UI but never passed to the
tool. Move anything the tool needs into `inputs` or `parameters`. Check the result with
`bilayers_cli generate <config.yaml> --cli`. See [Core Data Flow](../architecture/data_flow.md).

**My tool runs, but the app shows no results.**
The output-folder parameter needs `output_dir_set: True` and must be a `parameter`, not
`display_only`. That's how the app knows where to look for results. See
[Inside bilayers-targets](../architecture/targets.md#getting-results-out).

**Does every interface support every config field?**
Not yet. A few fields only affect some interfaces (for example `mode` only changes the
Jupyter layout, and `unique_string` only matters to the CellProfiler plugin). See the
table in [Inside bilayers-targets](../architecture/targets.md#which-config-fields-each-target-uses).

## Development

**Why is Bilayers four repositories?**
To version and test the schema, generators, algorithms, and orchestrator
independently. See [How Bilayers is Organized](../architecture/overview.md).

**I edited a sibling repo but the orchestrator doesn't see my change.**
The siblings are installed from git at the commit recorded in `pixi.lock`, not from
your checkout. Point the environment at your local checkout (pixi path dependency); see
[Local Setup](../developer_guide/dev_setup.md).

**CI is testing an older version of a sibling repo. Why?**
CI installs with `locked: true`, so it uses the sibling commits recorded in `pixi.lock`.
Run `pixi update` and commit the lockfile to move them forward. See
[Versioning & Reproducibility](../versioning/versioning.md).

**I changed a template and the regression test fails.**
That's expected when output changes on purpose: regenerate the golden files and review
the diff. See [Developer Testing](../testing/developer_testing.md).

**Still stuck?**
Ask in [GitHub Discussions](https://github.com/orgs/bilayer-containers/discussions) or
[open an issue](https://github.com/bilayer-containers/bilayers/issues).

<!-- TODO: add real user questions here as they come up in issues and discussions. -->
