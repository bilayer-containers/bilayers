---
title: Running Bilayers Docker Images
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers provides ready-to-use Docker images with Gradio or Jupyter Notebook interfaces for bioimage analysis algorithms. This guide explains how to pull and run these images via CLI (Command Line Interface) or Docker Desktop (GUI).

## 1. Pull the Docker Image (CLI or Docker Desktop)

**Available Docker Images:**
- classical_segmentation X Gradio :
  ```{code} bash
  docker pull bilayer/classical_segmentation:1.0.0-gradio 
  ```
- classical_segmentation X Jupyter_Notebook :
  ```{code} bash
  docker pull bilayer/classical_segmentation:1.0.0-jupyter 
  ```
- cellpose_inference X Gradio :
  ```{code} bash
  docker pull bilayer/cellpose:1.0.1-gradio
  ```
- cellpose_inference X Jupyter_Notebook :
  ```{code} bash
  docker pull bilayer/cellpose:1.0.0-jupyter
  ```
- instanseg_inference X Gradio :
  ```{code} bash
  docker pull bilayer/instanseg:1.0.2_pixi_gradio
  ```
- instanseg_inference X Jupyter :
  ```{code} bash
  docker pull bilayer/instanseg:1.0.2_pixi_jupyter
  ```

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

:::{attention}
**Volume Mount:** A volume mount allows a Docker container to access and store files on the host machine. This prevents data loss when the container stops. Running a Jupyter interface requires a volume mount for data persistence.

**No Volume Mount:** Without a volume mount, files inside the container don’t save outside it. Usually, ideal for temporary tasks that don’t need to keep data after stopping the container. Running a Gradio interface does not require a volume mount (you can download the output from the UI)
:::

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

- Gradio: Start the Image as-is, assign it a name, and select an available port (e.g., 8000 for Gradio)

![cellposeXgradio](../images/tool_user/cellposeXgradio.mp4)

---

- Jupyter: Use the Volume option to mount your data directory to /bilayers/input_images

![cellposeXgradio](../images/tool_user/cellposeXjupyter.mp4)
