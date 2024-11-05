---
title: Creating an Interface for Your Custom Algorithm
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers typoooooo allows you to easily create a web interface (using Gradio) or a Jupyter Notebook interface for any deep-learning cell segmentation algorithm by filling out a simple configuration file in YAML format. It’s as simple as filling out a Google Form!
Before you begin, let’s break down the key elements you need to know - 

1. [Interface](/supported-interfaces)
    - [What is Gradio?](/supported-interfaces#what-is-gradio)
    - [What is JupyterNB?](/supported-interfaces#what-is-a-jupyter-notebook)
2. [Understanding config.yaml requirements](/understanding-config)
    - [parameters](/understanding-config#defining-parameters)
    - [display_only](/understanding-config#defining-display-only)
    - [results](/understanding-config#defining-results)
    - [exec_function](/understanding-config#defining-exec-function)
    - [docker_image](/understanding-config#defining-docker-image)
    - [algorithm_folder_name](/understanding-config#defining-algorithm-folder-name)
    - [citations](/understanding-config#defining-citations)
3. [Steps to create your custom Algorithm’s Interfaces](/steps-to-create)
    - Step 0: Clone the repo
    - Step 1: Create your own Algorithm spec-file
    - Step 2: Use the custom Docker Images
    - Step 3: Raise the PR → Bilayers Team will approve and can publish the docker-image on docker-hub


