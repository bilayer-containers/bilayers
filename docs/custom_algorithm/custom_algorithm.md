---
title: Generating Interfaces for Custom Algorithms
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers simplifies the process of **creating web apps, notebooks, and plugins** for any **containerized bioimage analysis algorithm.**
Instead of writing extensive UI code, you only need to **fill out a structured YAML file**—just like filling out a **Google Form!**

## Before You Begin:
To successfully generate an interface, familiarize yourself with the key **Bilayers components:**

1. [Choosing the right base docker image](/right-base-docker-image)
   Your algorithm’s Docker image must meet Bilayers’ compatibility requirements. Follow these guidelines to ensure seamless integration:
    - [Requirements for the Algorithm (Base) Docker Image](/right-base-docker-image#requirements-for-the-algorithm-base-docker-image) - Must include Python, package managers, and other essentials
    - [Adapting Non-Compliant Base Images](/right-base-docker-image#adapting-non-compliant-base-images) - Steps to adjust an existing image to Bilayers requirements
2. [Supported Interfaces](/supported-interfaces)
   Bilayers currently supports the following targets:
    - [Gradio](/supported-interfaces#gradio) - A no code web UI
    - [Streamlit](/supported-interfaces#streamlit) - A no code web UI, alternative to Gradio
    - [Jupyter Notebook](/supported-interfaces#jupyter-notebook) - Interactive notebooks
    - [CellProfiler plugin](/supported-interfaces#cellprofiler-plugin) - A generated module for an existing CellProfiler installation, not a container
3. [Understanding config.yaml requirements](/understanding-config)
   The **config.yaml** file (the spec file) is a declarative description of your container: what it takes in, what it produces, and which knobs a user is allowed to turn. You write one per algorithm, and it lives in your algorithms folder in the  [bilayers-algorithms](https://github.com/bilayer-containers/bilayers-algorithms) repository.
4. [Steps to create your custom Algorithm’s Interfaces](/steps-to-create)
   Once you’ve selected an interface type, configured config.yaml, and prepared a compatible Docker image, follow the Step-by-Step Guide to generate your UI automatically.