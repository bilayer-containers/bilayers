import argparse
import os
import scipy
import skimage
import numpy


def example_function(image_list, threshold_method, min_size, max_size, save_dir):
    """
    Example function that will threshold, label, and then filter objects
    based on size. This function also saves the arrays and returns the
    file save paths, which can be downloaded by the user.
    """
    # Store output filenames to be returned
    output_filelist = list()

    for image_path in image_list:
        # Load the image
        print("My Input Image Path: ", image_path)
        image = skimage.io.imread(image_path)

        # Threshold the image
        if threshold_method.casefold() == "otsu":
            th_image = image > skimage.filters.threshold_otsu(image)
        elif threshold_method.casefold() == "li":
            th_image = image > skimage.filters.threshold_li(image)
        else:
            raise NotImplementedError

        # Label the image
        labeled_image = skimage.measure.label(th_image)

        areas = scipy.ndimage.sum(
            numpy.ones(labeled_image.shape),
            labeled_image,
            numpy.array(list(range(0, labeled_image.max() + 1)), dtype=numpy.int32),
        )
        areas = numpy.array(areas, dtype=int)
        min_allowed_area = numpy.pi * (min_size * min_size) / 4
        max_allowed_area = numpy.pi * (max_size * max_size) / 4
        # area_image has the area of the object at every pixel within the object
        area_image = areas[labeled_image]
        labeled_image[area_image < min_allowed_area] = 0
        labeled_image[area_image > max_allowed_area] = 0

        # Construct filename from input
        base_filename = os.path.basename(image_path).split(".")[0]
        output_filename = os.path.join(save_dir, base_filename + "_output.tiff")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Save file
        skimage.io.imsave(output_filename, labeled_image)
        print(f"Output saved to: {output_filename}")

        # Append output filename to the list
        output_filelist.append(output_filename)

    # Return the list of file names
    return output_filelist

def parse_arguments():
    """
    Parse the command-line arguments using argparse.
    """
    parser = argparse.ArgumentParser(
        description="Threshold images and filter objects by size."
    )

    parser.add_argument(
        "--folder",
        required=True,
        help="Path to the folder containing input images."
    )
    parser.add_argument(
        "--threshold_method",
        choices=["otsu", "li"],
        required=True,
        help="Thresholding method to use ('otsu' or 'li')."
    )
    parser.add_argument(
        "--min_size",
        type=float,
        required=True,
        help="Minimum size of objects to retain."
    )
    parser.add_argument(
        "--max_size",
        type=float,
        required=True,
        help="Maximum size of objects to retain."
    )

    parser.add_argument(
        "--save_dir",
        required=True,
        help="Path to the folder to save output images."
    )

    return parser.parse_args()


def get_image_files_from_folder(folder_path):
    """
    Get a list of image files from the specified folder.
    """
    # List of supported image file extensions
    image_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.tif']

    # Get all files in the folder and filter by image extensions and also dont include the files with _output in the name
    image_files = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if os.path.splitext(file)[1].lower() in image_extensions and "_output" not in file
    ]

    return image_files


def main():
    # Parse the arguments
    args = parse_arguments()

    # Get list of image files from the folder
    image_list = get_image_files_from_folder(args.folder)

    if not image_list:
        print("No images found in the specified folder.")
        return

    # Call the example function
    output_filelist = example_function(
        image_list=image_list,
        threshold_method=args.threshold_method,
        min_size=args.min_size,
        max_size=args.max_size,
        save_dir=args.save_dir
    )

    # Print the output file paths for the user to access
    for file_path in output_filelist:
        print(f"Output saved to: {file_path}")


if __name__ == "__main__":
    main()
