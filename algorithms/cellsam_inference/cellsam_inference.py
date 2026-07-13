import argparse
import os
import numpy as np
import skimage.io
import imageio

from cellSAM import get_model, segment_cellular_image


def cellsam_inference(model_name, input_folder, output_folder, device,
                      bbox_threshold, normalize_img, postprocess,
                      remove_boundaries, fast):
    """Run CellSAM segmentation on every image in a folder and save masks."""

    # Make sure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Collect valid image files, skipping any we already produced
    image_extensions = (".tif", ".tiff", ".png", ".jpg", ".jpeg", ".bmp", ".npy")
    image_files = [
        f
        for f in os.listdir(input_folder)
        if f.lower().endswith(image_extensions) and "_segmented" not in f
    ]

    if not image_files:
        print("Exiting... No valid image files found in the folder!")
        return

    print(f"Processing... Found {len(image_files)} images in {input_folder}...")

    # Load the model once, before the loop
    model = get_model(model_name)
    print(f"Model loaded: {model_name}")

    # Process each image
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        print(f"Loading image: {image_path}")

        # .npy images need np.load, everything else uses skimage
        if image_file.lower().endswith(".npy"):
            img = np.load(image_path)
        else:
            img = skimage.io.imread(image_path)

        mask, _, _ = segment_cellular_image(
            img,
            model=model,
            normalize=normalize_img,
            postprocess=postprocess,
            remove_boundaries=remove_boundaries,
            bbox_threshold=bbox_threshold,
            fast=fast,
            device=device,
        )

        # Build output name from input name
        output_image_path = os.path.join(
            output_folder, os.path.splitext(image_file)[0] + "_segmented.tif"
        )

        print(f"Saving result to {output_image_path}")
        imageio.imwrite(output_image_path, mask.astype(np.int32))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minimal CellSAM CLI for segmentation.")
    parser.add_argument("--model_name", type=str, default="cellsam_general",
                        choices=["cellsam_general", "cellsam_extra"],
                        help="Which CellSAM model to load.")
    parser.add_argument("--input_folder", type=str, required=True,
                        help="Path to folder of input images.")
    parser.add_argument("--output_folder", type=str, required=True,
                        help="Path to folder for output masks.")
    parser.add_argument("--device", type=str, default="cpu",
                        choices=["cpu", "cuda"],
                        help="Run on CPU or GPU.")
    parser.add_argument("--bbox_threshold", type=float, default=0.4,
                        help="Confidence cutoff for detecting cells.")
    # Default is on, so read "True"/"False" as a bool to let the checkbox turn it off.
    parser.add_argument("--normalize", type=lambda x: x.lower() == "true",
                    default=True,
                    help="Normalize the image before segmenting.")
    parser.add_argument("--postprocess", action="store_true",
                        help="Extra cleanup for noisy images.")
    parser.add_argument("--remove_boundaries", action="store_true",
                        help="Shave a one pixel edge off each cell.")
    parser.add_argument("--fast", action="store_true",
                        help="Batched inference. Faster, alpha feature.")

    args = parser.parse_args()

    cellsam_inference(
        args.model_name,
        args.input_folder,
        args.output_folder,
        args.device,
        args.bbox_threshold,
        args.normalize,
        args.postprocess,
        args.remove_boundaries,
        args.fast,
    )
