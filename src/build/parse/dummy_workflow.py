import subprocess

def run_segmentation(config_path):
    """Run segmentation step and package outputs into Docker."""
    print("Running segmentation step...")
    subprocess.run(["python", "src/build/parse/dummy_segmentation.py", config_path], check=True)

def run_post_processing(config_path):
    """Run post-segmentation step using Docker outputs."""
    print("Running post-segmentation step...")
    subprocess.run(["python", "src/build/parse/dummy_post_processing.py", config_path], check=True)

def main():
    config_path = "src/algorithms/cellpose_input_output/config.yaml"

    # Step 1: Segmentation
    run_segmentation(config_path)
    print("Segmentation completed successfully!")

    # Step 2: Post-Segmentation
    run_post_processing(config_path)

if __name__ == "__main__":
    main()