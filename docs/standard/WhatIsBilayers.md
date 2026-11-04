---
title: What is Bilayers?
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers is an **open-source specification** designed to characterize software containers in terms of expected inputs, outputs, and tunable parameters. Its primary aim is to make bioimage analysis deep-learning algorithms more accessible by automatically generating intuitive, no-terminal-required user interfaces. Bilayers ensures that software containers can be deployed consistently across different environments, from small prototypes to large-scale workflows, without the risk of version mismatch.

Bilayers currently supports four interfaces — **Gradio**, **Jupyter Notebook**, **Streamlit**, and a **CellProfiler plugin** — with more planned. Each algorithm paired with a Gradio, Jupyter, or Streamlit interface is containerized and published as a Docker image on DockerHub (the CellProfiler plugin is a generated module instead), allowing users to run the tool effortlessly by spinning up a Docker container. You can start using it right away — No Coding or Complicated Installations needed!


In addition to using pre-built Docker images provided by Bilayers, you can also create your own web interface or Jupyter Notebook interface for custom deep-learning algorithms. You can even fine-tune algorithms from the BioImage Model Zoo by simply filling out a configuration file (as long as the algorithm's Docker image is available on DockerHub). Bilayers offers a simple, interactive interface with widgets like number inputs, text fields, radio buttons, dropdown menus, image upload options and more. This makes it easy to tweak parameters and input your images for analysis, giving you the desired output with minimal effort.

It ensures that the same containerized algorithms used in prototypes can be reliably deployed in large-scale workflows without version drift, whether on local machines, high-performance computing (HPC) systems, or in the cloud. This also helps sysadmins create and validate workflows for end users in tools like Nextflow or Snakemake.

Bilayers is open-source, and we welcome contributions! You can create an interface for your custom deep-learning algorithm using Bilayers, and if you’d like, we can publish it on DockerHub to benefit the broader bioimaging community.

## What are containers?
Containers are lightweight piece of software that contains all the code, libraries, and dependencies that the application needs to run. Containers do not have their own operating system, they get resources from the host operating system. They are also easily portable as they contain all the libraries and the dependencies to run the application.

## What is Docker?
Docker is a containerization platform that allows you to package code and dependencies into a Docker image that can be run on any machine. It allows your application to be separated from your infrastructure. The image that you created is portable, so you can run it on any machine that has Docker installed.

## Quick Links

### Run a pre-built tool
No coding required — pull an image and use the UI. [User Guide](../user_guide/user_guide.md)

### Wrap your own algorithm
Describe your tool in a config and generate interfaces for it. [Wrap a New Algorithm](../developer_guide/wrap_algorithm.md)

### Understand how it works
The four-repo layout and the parse → generate pipeline. [Architecture](../architecture/overview.md)

### Contribute
Developer setup, testing, and PR workflow. [Developer Guide](../developer_guide/developer_guide.md)