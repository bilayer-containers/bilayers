---
title: Supported Interfaces
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers supports four targets, grouped into two families.

**Interfaces** are self-contained applications. Bilayers generates the application and layers it onto your algorithm image, producing a container you can run:

1. **Gradio** – A no-code web-based UI
2. **Streamlit** – A no-code web-based UI, an alternative to Gradio
3. **Jupyter Notebook** – An interactive coding environment

**Plugins** are generated source files for a tool the user already has. There is no container to run:

4. **CellProfiler Plugin** – A module for an existing CellProfiler installation



<br>

## Gradio
**Best for:** Users who want a simple, interactive web-based UI without coding.

Gradio provides a quick and easy way to demo your machine learning model through a user-friendly web interface, making it accessible to anyone, anywhere. [Learn More](https://www.gradio.app/)



## Streamlit

**Best for:** Users who want a web-based UI and prefer Streamlit's layout and widgets over Gradio's.

Streamlit turns Python scripts into shareable web apps with minimal effort. It covers the same ground as Gradio, so pick whichever suits your users better. [Learn More](https://streamlit.io/)

## Jupyter Notebook

**Best for:** Users who want to read, modify, and rerun the code that drives the algorithm.

Jupyter Notebooks offer a flexible, interactive environment where users can run and modify code. [Learn More](https://jupyter-notebook.readthedocs.io/en/latest/)


## CellProfiler Plugin

**Best for:** Users who already work in CellProfiler and want your algorithm as a step in an existing pipeline.

Unlike the interfaces above, this target produces a Python module rather than a container. Drop the generated file into your CellProfiler plugins directory and your algorithm appears as a module in the pipeline builder. [Learn More](https://plugins.cellprofiler.org/)

Bilayers derives the module's category from the combination of input and output types declared in your `config.yaml`, placing it under Image Processing, Image Segmentation, Object Processing, or Measurement. Some combinations have no CellProfiler equivalent, in which case plugin generation stops with an error, leaving the other targets unaffected.
