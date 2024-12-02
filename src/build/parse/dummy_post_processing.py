import os
import sys
from skimage import io
from scipy.ndimage import gaussian_filter
from dummy_parse import parse_config  # Import parse.py for spec parsing

def run_post_processing(input_image_path, output_dir):
    """
    Perform post-processing on the input image.
    
    Args:
        input_image_path (str): Path to the input image file.
        output_dir (str): Directory to save the processed image.
    """
    print(f"Processing image: {input_image_path}")
    try:
        # Load the image
        image = io.imread(input_image_path)
        
        # Apply Gaussian smoothing as an example of post-processing
        processed_image = gaussian_filter(image, sigma=1)

        # Save the processed image to the output directory
        os.makedirs(output_dir, exist_ok=True)
        output_image_path = os.path.join(output_dir, os.path.basename(input_image_path))
        io.imsave(output_image_path, processed_image)

        print(f"Processed image saved to: {output_image_path}")
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")

def main():
    # Step 1: Parse the spec file
    config_path = sys.argv[1] if len(sys.argv) > 1 else "src/algorithms/cellpose_input_output/config.yaml"
    config = parse_config(config_path)

    # Step 2: Extract the outputs section from the spec file
    outputs = config.get("outputs", [])

    # Define the directory to save processed outputs
    post_processing_output_dir = "src/build/parse/dummy/processed_outputs"

    # Step 3: Iterate over the outputs and process each image
    for output in outputs:
        # Extract the path of the output image
        output_path = output.get("path")
        if output_path and os.path.isfile(output_path):
            # Process the image
            run_post_processing(output_path, post_processing_output_dir)
        else:
            print(f"Skipping invalid or missing file: {output_path}")

if __name__ == "__main__":
    main()
