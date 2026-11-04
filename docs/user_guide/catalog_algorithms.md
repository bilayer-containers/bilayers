---
title: "Catalog: Algorithms"
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

The algorithms currently wrapped in Bilayers, grouped by category. Each lives in
[`bilayers-algorithms`](https://github.com/bilayer-containers/bilayers-algorithms) as a
folder with a `config.yaml`.

:::{note}
**This page will be auto-generated.** The plan
([#127](https://github.com/bilayer-containers/bilayers/issues/127)) is to populate this
catalog from each algorithm's `config.yaml` (name, category, description, citations,
docker image) so it never drifts. The table below is a manual placeholder until that
generator lands.
:::

## Segmentation

| Algorithm | Description | Base image (from `config.yaml`) | Published interface images |
| --- | --- | --- | --- |
| `cellpose_inference` | Cellpose deep-learning cell segmentation in microscopy images | `cellprofiler/runcellpose_no_pretrained:2.3.2` | `bilayer/cellpose` (Gradio, Jupyter) |
| `instanseg_inference` | InstanSeg nucleus segmentation in brightfield images | `bilayer/instanseg:1.0.2` | `bilayer/instanseg` (Gradio, Jupyter) |
| `stardist_inference` | StarDist star-convex object segmentation | `rajavishah/stardist:8.0.0` | none yet |
| `classical_segmentation` | Classical thresholding (Otsu or Li) with size filtering | `bilayer/classical_segmentation:1.0.0` | `bilayer/classical_segmentation` (Gradio, Jupyter) |

## Image processing

| Algorithm | Description | Base image (from `config.yaml`) | Published interface images |
| --- | --- | --- | --- |
| `gaussian_smoothing` | Gaussian blur with a user-chosen sigma | `bilayer/gaussian_smoothing:1.0.0` | `bilayer/gaussian_smoothing` (Gradio, Jupyter) |

See [Run a Bilayers Image](../tool_user/steps_to_run.md) for the exact tags to pull.
`bilayers-algorithms` also contains `example_algorithm`, an empty config template for
wrapping a new tool; it is not a runnable algorithm.

<!-- TODO: replace with an auto-generated table sourced from bilayers-algorithms configs (#127). -->
