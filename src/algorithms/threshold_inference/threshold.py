import scipy
import skimage
import os
import numpy

def example_function(image_list, threshold_method, min_size, max_size):
    """
    Example function that will threshold, label, and then filter objects
    based on size.

    This function also save the arrays and returns the file save paths. The file
    save paths will be read by gr.File and allow the user to download the
    analysed images.
    """
    # Store output filenames to be returned
    output_filelist = list()

    # Check: Type of image_list: To resolve 'list doesnt have attribute name'
    print(f"image_list type: {type(image_list)}")

    for image_path in image_list:
        # Load the image
        print("My Input Image Path: ", image_path)
        image = skimage.io.imread(image_path.name)
        

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
        base_dir = os.path.dirname(image_path)
        output_filename = os.path.join(base_dir, base_filename + "_output.tiff")
        
        # Save file
        skimage.io.imsave(output_filename, labeled_image)

        output_filelist.append(output_filename)

    # Return the list of file names
    return output_filelist
