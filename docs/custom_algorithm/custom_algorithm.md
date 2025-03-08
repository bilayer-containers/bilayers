---
title: Generating Interfaces for Custom Algorithm
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers simplifies the process of **creating web-based (Gradio) or Jupyter Notebook interfaces** for any **deep-learning cell segmentation algorithm.**
Instead of writing extensive UI code, you only need to **fill out a structured YAML file**—just like filling out a **Google Form!**

## Before You Begin:
To successfully generate an interface, familiarize yourself with the key **Bilayers components:**

1. [Supported Interfaces](/supported-interfaces)  
   Bilayers currently supports the following interface types:
    - [Gradio](/supported-interfaces#gradio) - A no code web UI
    - [Jupyter Notebook](/supported-interfaces#jupyter-notebook) - Interactive notebooks
2. [Understanding config.yaml requirements](/understanding-config)
   The **config.yaml** file defines the behavior of your interface, including input/output handling and algorithm execution.
Each section of this file serves a distinct purpose:
    - [citations](/understanding-config#defining-citations) - Reference publications or software licenses
    - [docker_image](/understanding-config#defining-docker-image) - Specify the pre-built Docker image
    - [algorithm_folder_name](/understanding-config#defining-algorithm-folder-name) - Define a workspace directory
    - [exec_function](/understanding-config#defining-exec-function) - Configure how the algorithm runs
    - [inputs](/understanding-config#defining-inputs) - Define expected input files/data
    - [outputs](/understanding-config#defining-outputs) - Specify expected results
    - [parameters](/understanding-config#defining-parameters) - Configure user-adjustable options
    - [display_only](/understanding-config#defining-display-only) - Read-only UI fields
3. [Choosing the right base docker image](/right-base-docker-image)
   Your algorithm’s Docker image must meet Bilayers’ compatibility requirements. Follow these guidelines to ensure seamless integration:
    - [Requirements for the Algorithm (Base) Docker Image](/right-base-docker-image#requirements-for-the-algorithm-base-docker-image) - Must include Python, package managers, and other essentials
    - [Adapting Non-Compliant Base Images](/right-base-docker-image#adapting-non-compliant-base-images) - Steps to modify an existing image
4. [Steps to create your custom Algorithm’s Interfaces](/steps-to-create)
   Once you’ve selected an interface type, configured config.yaml, and prepared a compatible Docker image, follow the Step-by-Step Guide to generate your UI automatically.