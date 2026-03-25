import os
import gradio as gr
import subprocess
import shutil
import zipfile
from typing import Any, Optional
import uuid
import datetime
import glob

def option_to_append(cli_tag: str, value: Any) -> str:
    """
    Formats CLI options for appending to the command.

    Args:
        cli_tag (str): CLI tag (e.g., "--option").
        value (Any): The value to append.

    Returns:
        str: The formatted CLI option.
    """
    if value is None:
        return ""
    
    if cli_tag == "":
        return str(value)  # Append only the value
    elif "=" in cli_tag:
        return f"{cli_tag}{value}"
    return f"{cli_tag} {value}"  # Append cli_tag and value

def cli_tag_is_valid(cli_tag: Optional[str]) -> bool:
    """
    Checks if the CLI tag is valid (not None, not "None", not empty)

    Args:
        cli_tag (Optional[str]): The CLI tag to check

    Returns:
        bool: True if valid, False otherwise
    """
    return cli_tag not in [None, "None", ""]


def generate_cli_command(
    cli_sequence: list[dict[str, Any]], 
    **kwargs: Any
    ) -> tuple[str, Optional[str], Optional[str]]:
    """
    Generates the CLI command dynamically based on pre-ordered CLI sequence and user inputs

    Args:
        cli_sequence (list[dict[str, Any]]): Pre-ordered sequence of inputs/parameters/hidden_args.
        **kwargs (Any): User-provided parameter values.

    Returns:
        tuple[str, Optional[str], Optional[str]]: CLI command, folder_name, and output_folder_name.
    """
    cli_command = ["python -m classical_segmentation"]


    folder_name = None
    output_folder_name = None

    # Iterate through the pre-ordered CLI sequence
    for item in cli_sequence:
        name = item.get("name", "")
        source = item.get("source", "")
        cli_tag = item.get("cli_tag", "")
        item_type = item.get("type", "")
        optional = item.get("optional", False)
        label = item.get("label", "")
        append_value = item.get("append_value", False)
        
        # Get value from kwargs (user input) or use default
        if source == "hidden":
            # Hidden arguments always use their configured value
            value = item.get("value", "")
        else:
            # Regular inputs/parameters: use user input if provided, else use default
            param_key = name.lower().replace(" ", "_")
            value = kwargs.get(param_key, item.get("default"))

        # Skip processing if value is None/empty and optional
        if value in [None, "", "None"] and optional:
            continue

        # Validate mandatory parameters
        if value in [None, "", "None"] and not optional:
            error_message = f"{label} needs to have some value. It's Mandatory!"
            raise gr.Error(error_message, duration=None)

        # Handle boolean types (checkbox)
        if isinstance(value, bool):
            if append_value:
                # Append both tag and value
                option = option_to_append(cli_tag, value)
                if option:
                    cli_command.append(option)
            else:
                # Only append tag if true
                if value and cli_tag and cli_tag_is_valid(cli_tag):
                    cli_command.append(cli_tag)

        # Handle list types (inputs with file/image/measurement/etc.)
        elif isinstance(value, list):
            folder_name = item.get("folder_name")
            if not folder_name:
                if optional:
                    # optional file input; nothing to do
                    continue
                raise gr.Error(f"{label}: folder_name missing in spec.", duration=None)

            if not value:  # just in case
                if optional:
                    continue
                raise gr.Error(f"{label} needs a file. It's Mandatory!", duration=None)

            os.makedirs(folder_name, exist_ok=True)
            for file_path in value:
                shutil.copy(file_path, folder_name)
            value = folder_name
            if cli_tag and cli_tag_is_valid(cli_tag):
                option = option_to_append(cli_tag, value)
                if option:
                    cli_command.append(option)

        # Handle text output paths, check if it has a directory-name i.e. it's coming for declaring output path
        elif isinstance(value, str) and item_type == "textbox" and item.get("output_dir_set"):
            # -------------------------------------------------------------
            # This section handles 3 major scenarios:
            #   (1) User explicitly provides an output directory name
            #   (2) User doesn't provide one - Bilayers creates a default
            #   (3) Algorithm manages its own outputs (no CLI tag)
            # -------------------------------------------------------------
            output_dir_set = item.get("output_dir_set", False)
            cli_tag_present = cli_tag_is_valid(cli_tag)
            
            # Determine base output folder:
            # - If the spec declares output_dir_set=True, use user's folder
            # - Otherwise, fall back to a default base folder ("outputs/")                
            base_output_dir = value if output_dir_set else item.get("default", "outputs")
            
            # Construct a unique run-specific subfolder name to prevent overwriting
            # Example: outputs/run_20251013_1910_ab12        
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_suffix = uuid.uuid4().hex[:4]
            unique_run_folder = os.path.join(base_output_dir, f"run_{timestamp}_{unique_suffix}")
            
            # Create new subfolder
            os.makedirs(unique_run_folder, exist_ok=True)
            output_folder_name = unique_run_folder
            
            if cli_tag_present:
                value = output_folder_name
                option = option_to_append(cli_tag, value)
                if option:
                    cli_command.append(option)

        # Handle all other types (radio, dropdown, textbox, number, etc.)
        elif value is not None:
            if value == "ignore":
                # Skip adding the whole "--cli_tag <value>" pair; if "ignore" is selected
                continue
            
            # Add to command if cli_tag is valid
            if cli_tag and cli_tag_is_valid(cli_tag):
                option = option_to_append(cli_tag, value)
                if option:
                    cli_command.append(option)

    return " ".join(cli_command), folder_name, output_folder_name

def create_zip_from_files(output_files: list[str], output_folder_name: Optional[str]) -> Optional[str]:
    """
    Creates a zip archive from the output files and returns the zip path
    """
    if not output_files:
        return None

    base_dir = output_folder_name or os.getcwd()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"outputs_{timestamp}.zip"
    zip_path = os.path.join(base_dir, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in output_files:
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=os.path.basename(file_path))

    return zip_path


# ---------------------------------------------------------------------------
# on_submit: function signature lists ALL parameters (including set_* / val_*)
# The val_* --> None suppression happens inside kwargs, not in the signature
# ---------------------------------------------------------------------------
def on_submit(

input_images_description,
input_images,

threshold_method,min_diameter,max_diameter,save_dir,

):

    kwargs = {
    
    
        "input_images": input_images,
    
    
    
    
    
    
        "threshold_method": threshold_method,
    
    
    
    
        "min_diameter": min_diameter,
    
    
    
    
        "max_diameter": max_diameter,
    
    
    
    
        "save_dir": save_dir,
    
    
    
    }

    print("Received parameters:", kwargs)

    # CLI sequence is passed in from the template context as a pre-ordered list
    cli_sequence = [{"cli_order": 0, "cli_tag": "--folder", "default": "directory", "depth": True, "description": "Upload all images to be analyzed", "file_count": "multiple", "folder_name": "/bilayers/input_images", "format": ["tiff", "ometiff", "png", "jpg", "jpeg"], "label": "Drag and drop all images to be analyzed", "mode": "beginner", "name": "input_images", "optional": False, "pyramidal": True, "section_id": "inputs", "source": "input", "subtype": ["grayscale", "color", "binary"], "tiled": True, "timepoints": True, "type": "image", "unique_string": ["*"]}, {"cli_tag": "--threshold_method", "default": "otsu", "description": "Select a threshold method to segment the image", "label": "Select a Threshold Method", "mode": "beginner", "name": "threshold_method", "optional": False, "options": [{"label": "otsu", "value": "otsu"}, {"label": "li", "value": "li"}], "section_id": "input-args", "source": "parameter", "type": "radio"}, {"cli_tag": "--min_size", "default": 5, "description": "Minimum diameter of objects in pixels", "label": "Object Minimum Diameter Size", "mode": "beginner", "name": "min_diameter", "optional": False, "section_id": "input-args", "source": "parameter", "type": "float"}, {"cli_tag": "--max_size", "default": 20, "description": "Maximum diameter of objects in pixels", "label": "Object Maximum Diameter Size", "mode": "beginner", "name": "max_diameter", "optional": False, "section_id": "input-args", "source": "parameter", "type": "float"}, {"cli_tag": "--save_dir", "default": "/bilayers/output_images", "description": "directory to save output files", "label": "Save Directory", "mode": "advanced", "name": "save_dir", "optional": True, "output_dir_set": True, "section_id": "output-args", "source": "parameter", "type": "textbox"}]

    # Generate the CLI command using the pre-ordered sequence
    cli_command, folder_name, output_folder_name = generate_cli_command(cli_sequence, **kwargs)
    print("Generated CLI command:", cli_command)

    # Execute the CLI command
    try:
        result = subprocess.run(cli_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command executed successfully")

        # Check if output_folder_name is not None and is a directory
        if output_folder_name and os.path.exists(output_folder_name) and os.path.isdir(output_folder_name):
            print("Folder exists")
            output_files = sorted([os.path.join(output_folder_name, f)
                            for f in os.listdir(output_folder_name)
                            if os.path.isfile(os.path.join(output_folder_name, f))])
        else:
            # Fallback: collect all generated files
            possible_files = []
            fallback_folder = "outputs_fallback"
            os.makedirs(fallback_folder, exist_ok=True)

            for root, _, files in os.walk("."):
                for f in files:
                    if f.startswith(".") or f.endswith((".py", ".pyc", ".ipynb")):
                        continue
                    full_path = os.path.join(root, f)
                    possible_files.append(full_path)
            
            fallback_folder = "outputs"
            os.makedirs(fallback_folder, exist_ok=True)
            
            # Copy all detected files into the fallback folder
            for file_path in possible_files:
                try:
                    shutil.copy(file_path, fallback_folder)
                except Exception as e:
                    print(f"Warning: could not copy {file_path}: {e}")

            output_files = sorted([
                os.path.join(fallback_folder, f)
                for f in os.listdir(fallback_folder)
                if os.path.isfile(os.path.join(fallback_folder, f))
            ])
            output_folder_name = fallback_folder
            print(f"Collected {len(output_files)} output files in: {fallback_folder}")

        zip_path = create_zip_from_files(output_files, output_folder_name)
        return output_files, zip_path

    except subprocess.CalledProcessError as e:
        error_message = "Please take a screenshot of this error and raise an issue at the Bilayers repository on GitHub."
        error_message += f"Command failed with error: {e.stderr.decode()}\n\n"
        raise gr.Error(error_message, duration=None)

# ---------------------------------------------------------------------------
# Component definitions
# These are defined at module level so they can be referenced both in
# all_parameters and inside the gr.Blocks event wiring below.
# ---------------------------------------------------------------------------




input_images_description = gr.Markdown(value="Upload all images to be analyzed")
input_images = gr.Files(label="Drag and drop all images to be analyzed", file_count="multiple")



















threshold_method = gr.Radio(
    label="Select a Threshold Method",
    info="Select a threshold method to segment the image",
    choices=[
        ("otsu", "otsu"), ("li", "li")
    ],
    value="otsu"
)








min_diameter = gr.Number(label="Object Minimum Diameter Size", info="Minimum diameter of objects in pixels", value=5 if "float" == "integer" else 5)








max_diameter = gr.Number(label="Object Maximum Diameter Size", info="Maximum diameter of objects in pixels", value=20 if "float" == "integer" else 20)








save_dir = gr.Textbox(label="Save Directory", info="directory to save output files", value="/bilayers/output_images", interactive=True)







# Ordered list of all input components passed to on_submit
all_parameters: list[Any] = [


input_images_description,
            input_images,
        


threshold_method,min_diameter,max_diameter,save_dir,



]

# ---------------------------------------------------------------------------
# gr.Blocks replaces gr.Interface here because gr.Interface does not support
# reactive event listeners like .change(). The Blocks context is required for
# the split-parameter checkbox --> number visibility wiring to work.
# ---------------------------------------------------------------------------
with gr.Blocks(title="Classical Segmentation - Brought to you in Gradio by Bilayers") as app:
    gr.Markdown("## Classical Segmentation - Brought to you in Gradio by Bilayers")
    gr.Markdown("""**This interface provides the following tool(s):**

Classical Segmentation: Segments images using classical thresholding methods : Otsu and Li

**This project relies on citations! Please cite ALL of the following if you find this application useful in your research:**

Cite Classical Segmentation using doi_number

Cite Gradio using 10.48550/arXiv.190602569

**Licenses of the components:**

Classical Segmentation is provided under the license_details license

Bilayers is provided under the BSD 3-Clause license

Gradio is provided under the Apache License 2.0 license""")

    with gr.Row():
        with gr.Column():
            
            
            
            input_images_description.render()
            input_images.render()
            
            

            
            threshold_method.render()
            
            min_diameter.render()
            
            max_diameter.render()
            
            save_dir.render()
            

            
            submit_btn = gr.Button("Run", variant="primary")

        with gr.Column():
            download_results_from_here = gr.Files(label="Download Output", file_count="multiple")
            download_all_zip = gr.DownloadButton(label="Download All (zip)")

    submit_btn.click(
        fn=on_submit,
        inputs=all_parameters,
        outputs=[download_results_from_here, download_all_zip],
    )

    
    

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7878, share=True)