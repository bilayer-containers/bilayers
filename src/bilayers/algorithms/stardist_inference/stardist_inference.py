import argparse
import os
import skimage.io
from skimage.transform import resize
import numpy as np
import imageio
from stardist.models import StarDist2D, StarDist3D
from csbdeep.utils import normalize


def stardist_inference(model_type, model_name, model_path, input_folder, output_folder, prob_thresh, nms_thresh, n_tiles_x, n_tiles_y, save_probs, use_gpu):
    """Run StarDist model for object detection and save results."""

    # Check if the output folder exists
    os.makedirs(os.path.dirname(output_folder), exist_ok=True)

    # Get list of all image files in the input folder
    image_extensions = (".tif", ".tiff", ".png", ".jpg", ".jpeg", ".bmp")
    image_files = [
        f
        for f in os.listdir(input_folder)
        if f.lower().endswith(image_extensions) and "_segmented" not in f and "_probabilities" not in f  # Exclude already segmented images
    ]

    # If not then raise an error
    if not image_files:
        print("Exiting... No valid image files found in the folder!")
        return

    print(f"Processing... Found {len(image_files)} images in {input_folder}...")

    # Load Model
    if model_type == "2D":
        if model_name:
            model = StarDist2D.from_pretrained(model_name)
        elif model_path:
            model = StarDist2D(None, basedir=os.path.dirname(model_path), name=os.path.basename(model_path))
        else:
            raise ValueError("You must specify either --model_name or --model_path for 2D.")
    elif model_type == "3D":
        if model_name:
            model = StarDist3D.from_pretrained(model_name)
        elif model_path:
            model = StarDist3D(None, basedir=os.path.dirname(model_path), name=os.path.basename(model_path))
        else:
            raise ValueError("You must specify either --model_name or --model_path for 3D.")
    else:
        raise ValueError("Invalid model type. Choose '2D' or '3D'.")

    print(f"Running inference with {model.__class__.__name__}")

    # Combine n_tiles_x and n_tiles_y into a list
    tiles = [n_tiles_x, n_tiles_y]

    print(f"Value of args.save_probabilities: {save_probs}")

    # Process all images
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        print(f"Loading image: {image_path}")

        img = skimage.io.imread(image_path)
        img = normalize(img)

        if not save_probs:
            print(f"Model loaded: {model}")
            # Probabilities aren't wanted, things are simple
            data = model.predict_instances(
                normalize(img),
                return_predict=False,
                n_tiles=tiles,
                prob_thresh=prob_thresh,
                nms_thresh=nms_thresh,
            )

            # Defining Output Filenames
            output_image_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + "_segmented.tif")

            # Save segmentation result
            print(f"Saving result to {output_folder}")
            imageio.imwrite(output_image_path, data[0])
        else:
            print("Coming here! - Else....")
            data, probs = model.predict_instances(
                normalize(img),
                return_predict=True,
                sparse=False,
                n_tiles=tiles,
                prob_thresh=prob_thresh,
                nms_thresh=nms_thresh,
            )

            # Save segmentation result
            output_image_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + "_segmented.tif")
            output_prob_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + "_probabilities.npy")

            # Save segmentation result
            print(f"Saving result to {output_image_path}")
            imageio.imwrite(output_image_path, data[0])

            size_corrected = resize(probs[0], img.shape)
            print(f"Type of size_corrected: {type(size_corrected)}")

            print(f"Saving probabilities to {output_prob_path}")
            imageio.imwrite(output_prob_path, size_corrected)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minimal StarDist CLI for segmentation.")
    parser.add_argument("--model_type", choices=["2D", "3D"], required=True, help="Choose StarDist model type.")
    parser.add_argument("--model_name", type=str, default=None, help="Pre-trained model name (if using a default model).")
    parser.add_argument("--model_path", type=str, default=None, help="Path to custom-trained model directory.")
    parser.add_argument("--input_folder", type=str, required=True, help="Path to input image.")
    parser.add_argument("--output_folder", type=str, default="output.tif", help="Output file name.")
    parser.add_argument("--prob_thresh", type=float, default=0.5, help="Probability threshold for detection.")
    parser.add_argument("--nms_thresh", type=float, default=0.4, help="Non-Maximum Suppression (NMS) threshold.")
    parser.add_argument("--n_tiles_x", type=int, default=1, help="Specify the number of tiles to break the image down into along the x-axis (horizontal).")
    parser.add_argument("--n_tiles_y", type=int, default=1, help="Specify the number of tiles to break the image down into along the y-axis (vertical).")
    parser.add_argument("--save_probabilities", action="store_false", help="Save probability map as a separate image.")
    parser.add_argument("--gpu", action="store_true", help="Use GPU for inference if available.")

    args = parser.parse_args()

    stardist_inference(
        args.model_type,
        args.model_name,
        args.model_path,
        args.input_folder,
        args.output_folder,
        args.prob_thresh,
        args.nms_thresh,
        args.n_tiles_x,
        args.n_tiles_y,
        args.save_probabilities,
        args.gpu,
    )
