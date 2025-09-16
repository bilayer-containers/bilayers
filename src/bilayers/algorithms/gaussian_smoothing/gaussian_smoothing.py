import argparse
import os
import skimage.io
import skimage.filters
import numpy
from typing import Any, TypedDict
from numpy.typing import NDArray


class ParsedArgs(TypedDict):
    folder: str
    threshold_method: str
    min_size: float
    max_size: float
    save_dir: str


def example_function(image_list: list[str], sigma_size: float, save_dir: str) -> list[str]:
    """
    Example function that will smooth images. This function 
    also saves the arrays and returns the
    file save paths, which can be downloaded by the user.

    Args:
        image_list (list[str]): list of image file paths to process.
        sigma_size (float): Size of gaussian blur to perform.
        save_dir (str): Path to the folder to save output images.

    Returns:
        list[str]: list of file paths of the saved output images.
    """
    # If no images are provided, return an empty list
    if not image_list:
        print("No images found in the specified folder.")
        return []

    # Store output filenames to be returned
    output_filelist: list[str] = []

    for image_path in image_list:
        # Load the image
        print("Processing Image: ", image_path)
        image: NDArray[Any] = skimage.io.imread(image_path)

        # Blur the image
        blur_image: NDArray[Any] = skimage.filters.gaussian(image,sigma_size)

        # Construct filename from input
        base_filename: str = os.path.basename(image_path).split(".")[0]
        output_filename: str = os.path.join(save_dir, base_filename + "_output.tiff")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Save file
        skimage.io.imsave(output_filename, blur_image)
        print(f"Output saved to: {output_filename}")

        # Append output filename to the list
        output_filelist.append(output_filename)

    # Return the list of file names
    return output_filelist


def parse_arguments() -> ParsedArgs:
    """
    Parse the command-line arguments using argparse.

    Returns:
        ParsedArgs: Parsed Command-Line Arguments.
    """
    parser = argparse.ArgumentParser(description="Threshold images and filter objects by size.")

    parser.add_argument("--folder", required=True, help="Path to the folder containing input images.")
    parser.add_argument("--sigma_size", type=float, required=True, help="Size of sigma to use for blurring")

    parser.add_argument("--save_dir", required=True, help="Path to the folder to save output images.")

    return vars(parser.parse_args())  # type: ignore


def get_image_files_from_folder(folder_path: str) -> list[str]:
    """
    Get a list of image files from the specified folder.

    Args:
        folder_path (str): Path to the folder containing images.

    Returns:
        list[str]: list of image file paths.
    """
    # list of supported image file extensions
    image_extensions: list[str] = [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".tif"]

    # Get all files in the folder and filter by image extensions and also dont include the files with _output in the name
    image_files: list[str] = [
        os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.splitext(file)[1].lower() in image_extensions and "_output" not in file
    ]

    return image_files


def main() -> None:
    """
    Main execution function that parses arguments, processes images, and saves outputs.
    """
    # Parse the arguments
    args: dict = parse_arguments()

    # Get list of image files from the folder
    image_list: list[str] = get_image_files_from_folder(args["folder"])

    if not image_list:
        print("No images found in the specified folder.")
        return

    # Call the example function
    output_filelist: list[str] = example_function(
        image_list=image_list, sigma_size=args["sigma_size"],  save_dir=args["save_dir"]
    )

    # Print the output file paths for the user to access
    for file_path in output_filelist:
        print(f"Output saved to: {file_path}")


if __name__ == "__main__":
    main()
