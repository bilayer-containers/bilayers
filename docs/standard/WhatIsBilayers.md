---
title: Bilayers
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

## Browse the Catalog

If you're here to analyze images, start with the catalog. Each tool runs in a Docker container on your computer, and you use it from your web browser.

::::{grid} 1 1 2 2

:::{card} Algorithms
:link: ../user_guide/catalog_algorithms.md
**Cellpose, StarDist, InstanSeg, classical segmentation, Gaussian smoothing**

What each tool does and which image to pull.
:::

:::{card} Interfaces
:link: ../user_guide/catalog_interfaces.md
**Gradio, Jupyter Notebook, Streamlit, CellProfiler plugin**

The different ways you can work with a tool, and what each one looks like.
:::

::::

## What is Bilayers?

A lot of good bioimage analysis software only runs from the command line, which keeps it out of reach for many of the biologists it was written for. Bilayers is our attempt to fix that.

Bilayers is an open-source specification for describing a containerized tool: the files it takes in, the files it produces, and the parameters you can adjust. A tool is described once, in a single `config.yaml`. From that file, Bilayers generates user interfaces for it. You get a Gradio or Streamlit web app, a Jupyter notebook, or a CellProfiler plugin, with the right widgets for each parameter (number fields, dropdowns, checkboxes, image uploads).

Each web app or notebook is packaged together with the tool into a Docker image and published on DockerHub. To use one, you pull the image, start it, and open it in your browser. You don't need to install Python, set up dependencies, or type commands.

### One container, from laptop to cluster

The container you use to try a tool on a few images is the same one you can run on an HPC cluster or in the cloud later. Since the software inside never changes, results don't drift between versions. This also helps people building larger pipelines in Nextflow or Snakemake: they can test a step interactively, then use the same image in production.

### Bring your own tool

If your tool has a command-line interface and a Docker image, you can wrap it. You write the `config.yaml` (by hand, or with a form like the [Bilayers Config Generator](https://bilayer-containers.github.io/bilayers-config-generator/)), and Bilayers generates the interfaces. If you'd like to share it, open a pull request and we can publish the images for others to use. See [Wrap a New Algorithm](../developer_guide/wrap_algorithm.md) to get started.

## Containers and Docker, briefly

A **container** bundles a program together with everything it needs to run: code, libraries, and system dependencies. Containers share the host computer's operating system rather than carrying their own, so they're much lighter than a virtual machine. Because everything is inside, a container behaves the same no matter which machine it runs on.

**Docker** is the most widely used tool for building and running containers. A Docker *image* is the packaged program. You can download it from a registry like DockerHub and run it on any computer that has Docker (or Podman) installed. Bilayers publishes its tools as Docker images for this reason.

## Where to go next

- **Watch the introduction.** A short video overview, plus slides and posters, on [Talks & Tutorials](../resources/talks_tutorials.md).
- **Run a tool.** Pull an image and open the interface. See the [User Guide](../user_guide/user_guide.md).
- **Wrap your own tool.** Describe it in a config and generate interfaces. See [Wrap a New Algorithm](../developer_guide/wrap_algorithm.md).
- **See how it works.** The four repositories and how a config becomes an interface. See [Architecture](../architecture/overview.md).
- **Contribute.** Local setup, testing, and the PR workflow. See the [Developer Guide](../developer_guide/developer_guide.md).
