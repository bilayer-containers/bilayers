---
title: Running Bilayers Docker Images
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Bilayers provides ready-to-use Docker images that pair a bioimage analysis algorithm with an interface (Gradio, Jupyter Notebook, or Streamlit). This guide explains how to pull and run these images from the command line or from Docker Desktop.

## 1. Pull the Docker Image (CLI or Docker Desktop)

**Available Docker Images:**

| Algorithm | Gradio | Jupyter Notebook |
| --- | --- | --- |
| classical_segmentation | `bilayer/classical_segmentation:1.0.0-gradio` | `bilayer/classical_segmentation:1.0.0-jupyter` |
| gaussian_smoothing | `bilayer/gaussian_smoothing:1.0.0-gradio` | `bilayer/gaussian_smoothing:1.0.0-jupyter` |
| cellpose_inference | `bilayer/cellpose:1.0.1-gradio` | `bilayer/cellpose:1.0.0-jupyter` |
| instanseg_inference | `bilayer/instanseg:1.0.2_pixi_gradio` | `bilayer/instanseg:1.0.2_pixi_jupyter` |

Images built by the current pipeline are named `bilayer/<algorithm>:<version>-<interface>`
(see [Versioning & Reproducibility](../versioning/versioning.md)); the cellpose and instanseg
images above predate that scheme. The full list of tags is on
[DockerHub](https://hub.docker.com/u/bilayer).

**Using CLI:**
- Open a terminal and run:

```{code-block} bash
docker pull bilayer/<repo_name>:<tag>
```
:::{note}
Replace ```<repo_name>``` and ```<tag>``` with an image from the table above, e.g. `bilayer/classical_segmentation:1.0.0-gradio`
:::

**Using Docker Desktop (GUI):**
- Open Docker Desktop, go to the Images tab, and search for ```bilayer```
- Pull the image directly from DockerHub

## 2. Run the Docker Container (CLI or Docker Desktop)

Each interface is a web page served from inside the container, so you must publish its
port with `-p` to open it in your browser:

| Interface | Port | Open in your browser |
| --- | --- | --- |
| Gradio | `7878` | `http://localhost:7878` |
| Jupyter Notebook | `7878` | the `http://127.0.0.1:7878/...?token=...` link printed in the terminal |
| Streamlit | `8501` | `http://localhost:8501` |

:::{attention}
**Volume Mount:** A volume mount allows a Docker container to access and store files on the host machine. This prevents data loss when the container stops. Running a Jupyter interface requires a volume mount for data persistence.

**No Volume Mount:** Without a volume mount, files inside the container don’t save outside it. Usually, ideal for temporary tasks that don’t need to keep data after stopping the container. Running a Gradio interface does not require a volume mount (you can download the outputs from the UI as a zip file)
:::

**Using CLI:**
- **Gradio Interface (No Volume Mount)**:
```{code-block} bash
docker run -it --rm -p 7878:7878 bilayer/<repo_name>:<tag>
```
- **Jupyter Interface (Requires Volume Mount):**
```{code-block} bash
docker run -it --rm -p 7878:7878 -v /path/to/your/data:/bilayers/input_images bilayer/<repo_name>:<tag>
```
:::{note}
Replace ```/path/to/your/data``` with your ```local directory``` for input images
:::

:::{warning}
Gradio apps are launched with `share=True`, so besides `localhost` Gradio also prints a temporary public `*.gradio.live` link. Anyone with that link can use the app while the container runs; don't share it if your images are confidential.
:::

**Using Docker Desktop (GUI):**

- Gradio: Start the Image, assign it a name, and under Ports map host port `7878` to the container's `7878`

![cellposeXgradio](../images/tool_user/cellposeXgradio.mp4)

---

- Jupyter: Map host port `7878` to the container's `7878`, and use the Volume option to mount your data directory to `/bilayers/input_images`

![cellposeXjupyter](../images/tool_user/cellposeXjupyter.mp4)
