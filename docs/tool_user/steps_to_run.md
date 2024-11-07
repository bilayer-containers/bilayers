---
title: Steps to Run Bilayers Docker Images
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---


## 1. Pull the Docker Image (CLI or Docker Desktop)

**Available Docker Images:**
- classical_segmentation X Gradio :
  ```{code}
  docker pull bilayer/classical_segmentation:1.0.0-gradio 
  ```
- classical_segmentation X Jupyter_Notebook :
  ```{code}
  docker pull bilayer/classical_segmentation:1.0.0-jupyter 
  ```
- cellpose_inference X Gradio :
  ```{code}
  docker pull bilayer/cellpose:1.0.1-gradio
  ```
- cellpose_inference X Jupyter_Notebook :
  ```{code}
  docker pull bilayer/cellpose:1.0.0-jupyter
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
**Volume Mount:** A volume mount lets a Docker container access and store files on the host machine, so data isn’t lost when the container stops or restarts.

**No Volume Mount:** Without a volume mount, files inside the container don’t save outside it. Usually, ideal for temporary tasks that don’t need to keep data after stopping the container. However, with Gradio, you can download your output if needed.
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
