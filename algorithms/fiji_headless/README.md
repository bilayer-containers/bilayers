# Fiji Headless Threshold Segmentation

## Overview

This algorithm performs simple intensity-threshold segmentation on single‑channel grayscale images using Fiji (ImageJ) in headless mode; it is a minimal, ready‑to‑run example showing how to run an ImageJ macro within the Bilayers framework to produce binary masks. 

It accepts a single‑channel image and a user‑defined threshold (0–255), converts pixels with intensity ≥ threshold to foreground (255) and pixels below to background (0), and saves the resulting binary TIFF mask alongside the original image for downstream analysis. 

It demos with a quick foreground/background separation, preprocessing for analysis pipelines, and serving as a template for integrating ImageJ macros into Bilayers, with minimal dependencies limited to the Fiji Docker image and the included [threshold.ijm](./threshold.ijm) macro.

## What Does This Algorithm Do?

The algorithm:
1. Loads a single-channel grayscale image
2. Applies a threshold value (0-255) specified by the user
3. Converts pixels above the threshold to white (255) and below to black (0)
4. Saves the resulting binary mask as a TIFF file

This is useful for:
- Segmenting bright objects on dark backgrounds
- Creating binary masks for further analysis
- Quick intensity-based object detection
- Preprocessing for downstream image analysis workflows

## Parameters

### Inputs
- **Input Image**: Single-channel grayscale image (supports TIFF, PNG, JPEG formats)

### Parameters
- **Threshold Value**: Integer between 0-255 (default: 128)
  - Pixels with intensity ≥ threshold → white (255)
  - Pixels with intensity < threshold → black (0)
  - Lower values detect dimmer objects
  - Higher values detect only bright objects

### Outputs
- **Output Directory**: Contains the thresholded binary mask saved as `<original_filename>_threshold.tif`

## Docker Image

This algorithm uses a custom build of Fiji Docker image from [Dockerfile](./Dockerfile).

## How It Works

The algorithm runs Fiji in headless mode (no GUI) using an ImageJ macro script (`threshold.ijm`). The macro:
1. Receives the input image path, output directory, and threshold value
2. Opens the image
3. Applies the threshold using ImageJ's `setThreshold()` function
4. Converts to a binary mask
5. Saves the result

## Usage

### Setup and Testing

1. **Add the algorithm to your Bilayers repository**:
   - Navigate to `src/bilayers/algorithms/fiji_headless`
   - Ensure all files (`__init__.py`, `config.yaml`, `threshold.ijm`, `Dockerfile`) are present

2. **Update CI/CD Configuration**:
   - Edit `scripts/build_docker.sh` at line #7:
     ```bash
     ALGORITHM_NAMES=("fiji_headless")
     ```
   - Edit `scripts/validate.sh` at line #6:
     ```bash
     ALGORITHM_NAMES=("fiji_headless")
     ```

3. **Build and test Docker images locally**:
   ```bash
   ./scripts/build_docker.sh --algorithm fiji_headless --interface gradio
   ```

4. **Test the algorithm**:
   ```bash
   docker run -it -p --rm 7878:7878 bilayer/fiji_headless:build-candidate
   ```

   Then open your browser to `http://localhost:7878` to access the Gradio interface.

5. **Push to your DockerHub repository**:
   ```bash
   docker build -t your-dockerhub-repo/fiji_headless:latest .
   docker push your-dockerhub-repo/fiji_headless:latest
   ```

For complete setup instructions, see [Steps to Create Custom Algorithm](../../docs/custom_algorithm/steps_to_create.md).