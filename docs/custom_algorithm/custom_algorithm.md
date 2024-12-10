---
title: Generating Interfaces for Custom Algorithm
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers allows you to easily create a web interface (using Gradio) or a Jupyter Notebook interface for any deep-learning cell segmentation algorithm by filling out a simple configuration file in YAML format. It’s as simple as filling out a Google Form!
Before you begin, let’s break down the key elements you need to know - 

1. [Supported Interface](/supported-interfaces)
    - [Gradio](/supported-interfaces#gradio)
    - [Jupyter Notebook](/supported-interfaces#jupyter-notebook)
2. [Understanding config.yaml requirements](/understanding-config)
    - [parameters](/understanding-config#defining-parameters)
    - [display_only](/understanding-config#defining-display-only)
    - [results](/understanding-config#defining-results)
    - [exec_function](/understanding-config#defining-exec-function)
    - [docker_image](/understanding-config#defining-docker-image)
    - [algorithm_folder_name](/understanding-config#defining-algorithm-folder-name)
    - [citations](/understanding-config#defining-citations)
3. [Choosing the right base docker image](/right-base-docker-image)
    - [Requirements for the Algorithm (Base) Docker Image](/right-base-docker-image#requirements-for-the-algorithm-base-docker-image)
    - [Adapting Non-Compliant Base Images](/right-base-docker-image#adapting-non-compliant-base-images)
4. [Steps to create your custom Algorithm’s Interfaces](/steps-to-create)
    


