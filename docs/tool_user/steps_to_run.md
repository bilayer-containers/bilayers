---
title: Steps to Run Bilayers Docker Images
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---


## 1. Pull the Docker Image (CLI or Docker Desktop)

**Using CLI:**
- Open a terminal and run:

```{code-block} bash
docker pull bilayer/<repo_name>:<tag>
```
:::{note}
Replace ```<repo_name>``` with the algorithm name (e.g., cellpose) and ```<tag>``` with the version (e.g., latest)
:::

**Using Docker Desktop (GUI):**
- Open Docker Desktop, go to the Images tab, and search for ```bilayer```
- Pull the image directly from DockerHub

## 2. Run the Docker Container (CLI or Docker Desktop)

**Using CLI:**
- **Gradio Interface (No Volume Mount)**:
```{code-block} bash
docker run -it --rm bilayer/<repo_name>:<tag>
```
- **Jupyter Interface (Requires Volume Mount):**
```{code-block} bash
docker run -it --rm -v /path/to/your/data:/bilayers/input_images bilayer/<repo_name>:<tag>
```
:::{note}
Replace ```/path/to/your/data``` with your ```local directory``` for input images
:::

**Using Docker Desktop (GUI):**
In the Containers tab, create a new container:
- Gradio: Start the container as-is, assign it a name, and select an available port (e.g., 8000 for Gradio)

![cellposeXgradio](../images/tool_user/cellposeXgradio.mp4)

---

- Jupyter: Use the Volume option to mount your data directory to /bilayers/input_images

![cellposeXgradio](../images/tool_user/cellposeXjupyter.mp4)
