import argparse
import os
import scipy.ndimage  # type: ignore
import skimage.io
import skimage.filters
import skimage.measure
import numpy
from typing import Any, TypedDict
from numpy.typing import NDArray


class ParsedArgs(TypedDict):
    folder: str
    threshold_method: str
    min_size: float
    max_size: float
    save_dir: str


def example_function(image_list: list[str], threshold_method: str, min_size: float, max_size: float, save_dir: str) -> list[str]:
    """
    Example function that will threshold, label, and then filter objects
    based on size. This function also saves the arrays and returns the
    file save paths, which can be downloaded by the user.

    Args:
        image_list (list[str]): list of image file paths to process.
        threshold_method (str): Thresholding method to use ('otsu' or 'li').
        min_size (float): Minimum size of objects to retain.
        max_size (float): Maximum size of objects to retain.
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

        # Threshold the image
        if threshold_method.casefold() == "otsu":
            th_image: NDArray[Any] = image > skimage.filters.threshold_otsu(image)
        elif threshold_method.casefold() == "li":
            th_image: NDArray[Any] = image > skimage.filters.threshold_li(image)
        else:
            raise NotImplementedError(f"Threshold method '{threshold_method}' is not implemented.")

        # Label the image
        # return_num=False ensures only an array is returned, hence type ignore is used
        label_image: NDArray[Any] = skimage.measure.label(th_image)  # type: ignore

        areas: NDArray[Any] = scipy.ndimage.sum(
            numpy.ones(label_image.shape),
            label_image,
            numpy.array(list(range(0, label_image.max() + 1)), dtype=numpy.int32),
        )
        areas = numpy.array(areas, dtype=int)
        min_allowed_area: float = numpy.pi * (min_size * min_size) / 4
        max_allowed_area: float = numpy.pi * (max_size * max_size) / 4
        # area_image has the area of the object at every pixel within the object
        area_image: NDArray[Any] = areas[label_image]
        label_image[area_image < min_allowed_area] = 0
        label_image[area_image > max_allowed_area] = 0

        # Construct filename from input
        base_filename: str = os.path.basename(image_path).split(".")[0]
        output_filename: str = os.path.join(save_dir, base_filename + "_output.tiff")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Save file
        skimage.io.imsave(output_filename, label_image)
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
    parser.add_argument("--threshold_method", choices=["otsu", "li"], required=True, help="Thresholding method to use ('otsu' or 'li').")
    parser.add_argument("--min_size", type=float, required=True, help="Minimum size of objects to retain.")
    parser.add_argument("--max_size", type=float, required=True, help="Maximum size of objects to retain.")

    parser.add_argument("--save_dir", required=True, help="Path to the folder to save output images.")

    return parser.parse_args()  # type: ignore


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
    args: ParsedArgs = parse_arguments()

    # Get list of image files from the folder
    image_list: list[str] = get_image_files_from_folder(args["folder"])

    if not image_list:
        print("No images found in the specified folder.")
        return

    # Call the example function
    output_filelist: list[str] = example_function(
        image_list=image_list, threshold_method=args["threshold_method"], min_size=args["min_size"], max_size=args["max_size"], save_dir=args["save_dir"]
    )

    # Print the output file paths for the user to access
    for file_path in output_filelist:
        print(f"Output saved to: {file_path}")


if __name__ == "__main__":
    main()
