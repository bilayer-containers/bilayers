import os
import glob
import streamlit as st
import subprocess
import shutil
import pathlib
from typing import Any, Optional
import uuid
import datetime

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

    # Radio options mapping
    radio_options = {
    
    "threshold_method": {
            "otsu": "otsu", "li": "li"
        },
    
    }

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
            raise Exception(error_message)

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
                raise Exception(f"{label}: folder_name missing in spec.")

            if not value:  # just in case
                if optional:
                    continue
                raise Exception(f"{label} needs a file. It's Mandatory!")

            os.makedirs(folder_name, exist_ok=True)
            for file_path in value:
                shutil.copy(file_path, folder_name)
            value = folder_name
            if cli_tag and cli_tag_is_valid(cli_tag):
                option = option_to_append(cli_tag, value)
                if option:
                    cli_command.append(option)

        # Handle text output paths, check if it has a directory-name i.e. it's coming for declaring ouput path
        elif isinstance(value, str) and item_type == "textbox" and item.get("output_dir_set"):
            # -------------------------------------------------------------
            # This section handles 3 major scenarios:
            #   (1) User explicitly provides an output directory name
            #   (2) User doesn’t provide one - Bilayers creates a default
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
            # Map radio/dropdown selections to values
            param_key = name.lower().replace(" ", "_")
            if param_key in radio_options and value in radio_options[param_key]:
                value = radio_options[param_key].get(value, value)
                
                if value == "ignore":
                    # Skip adding the whole "--cli_tag <value>" pair; if "ignore" is selected
                    continue
            
            # Add to command if cli_tag is valid
            if cli_tag and cli_tag_is_valid(cli_tag):
                option = option_to_append(cli_tag, value)
                if option:
                    cli_command.append(option)

    return " ".join(cli_command), folder_name, output_folder_name

# Dynamically define on_submit with the exact parameter arguments
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

    # Mapping of parameter tags to CLI tags
    cli_tags = {
    
    "input_images": {
        "cli_tag": "--folder",
        "default": "directory",
        "cli_order": 0,
        "optional": False,
        "label": "Drag and drop all images to be analyzed",
        
        "folder_name": "/bilayers/input_images"
        
    },
    
    
    "threshold_method": {
        "cli_tag": "--threshold_method",
        "default": "otsu",
        "cli_order": 0,
        "optional": False,
        "label": "Select a Threshold Method",
        
        
    },
    
    "min_diameter": {
        "cli_tag": "--min_size",
        "default": "5",
        "cli_order": 0,
        "optional": False,
        "label": "Object Minimum Diameter Size",
        
        
    },
    
    "max_diameter": {
        "cli_tag": "--max_size",
        "default": "20",
        "cli_order": 0,
        "optional": False,
        "label": "Object Maximum Diameter Size",
        
        
    },
    
    "save_dir": {
        "cli_tag": "--save_dir",
        "default": "/bilayers/output_images",
        "cli_order": 0,
        "optional": True,
        "label": "Save Directory",
        
        
        "output_dir_set": True,
        
    }
    
    }

    print("Received parameters:", kwargs)

    # CLI sequence is passed in from the template context as a pre-ordered list
    cli_sequence = [{"cli_order": 0, "cli_tag": "--folder", "default": "directory", "depth": True, "description": "Upload all images to be analyzed", "file_count": "multiple", "folder_name": "/bilayers/input_images", "format": ["tiff", "ometiff", "png", "jpg", "jpeg"], "label": "Drag and drop all images to be analyzed", "mode": "beginner", "name": "input_images", "optional": False, "pyramidal": True, "section_id": "inputs", "source": "input", "subtype": ["grayscale", "color", "binary"], "tiled": True, "timepoints": True, "type": "image", "unique_string": ["*"]}, {"cli_tag": "--threshold_method", "default": "otsu", "description": "Select a threshold method to segment the image", "label": "Select a Threshold Method", "mode": "beginner", "name": "threshold_method", "optional": False, "options": [{"label": "otsu", "value": "otsu"}, {"label": "li", "value": "li"}], "section_id": "input-args", "source": "parameter", "type": "radio"}, {"cli_tag": "--min_size", "default": 5, "description": "Minimum diameter of objects in pixels", "label": "Object Minimum Diameter Size", "mode": "beginner", "name": "min_diameter", "optional": False, "section_id": "input-args", "source": "parameter", "type": "float"}, {"cli_tag": "--max_size", "default": 20, "description": "Maximum diameter of objects in pixels", "label": "Object Maximum Diameter Size", "mode": "beginner", "name": "max_diameter", "optional": False, "section_id": "input-args", "source": "parameter", "type": "float"}, {"cli_tag": "--save_dir", "default": "/bilayers/output_images", "description": "directory to save output files", "label": "Save Directory", "mode": "advanced", "name": "save_dir", "optional": True, "output_dir_set": True, "section_id": "output-args", "source": "parameter", "type": "textbox"}]

    # Generate the CLI command using the pre-ordered sequence
    cli_command, folder_name, output_folder_name = generate_cli_command(cli_sequence, **kwargs)
    print("Generated CLI command:", cli_command)

    if output_folder_name is None:
        #we don't know the output folder name, so we will track the input folder(s) for newly modified files
        existing_input_files = {}
        
        existing_input_files["/bilayers/input_images"] = [(x,pathlib.Path(x).stat().st_mtime) for x in glob.glob(f"/bilayers/input_images/*")]
        

    # Execute the CLI command
    try:
        result = subprocess.run(cli_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command executed successfully")

        # Check if output_folder_name is not None and is a directory
        if output_folder_name and os.path.exists(output_folder_name) and os.path.isdir(output_folder_name):
            print("Folder exists")
            # Display Output files
            output_files = [os.path.join(output_folder_name, f) for f in os.listdir(output_folder_name) if os.path.isfile(os.path.join(output_folder_name, f))]
        else:
            print("Folder does not exist or output_folder_name is None")
            output_files = []
            if output_folder_name == None:
                for eachinputfolder, eachorigfiles in existing_input_files.items():
                    for filecandidate in glob.glob(f"{eachinputfolder}/*"):
                        if (filecandidate,pathlib.Path(filecandidate).stat().st_mtime) not in eachorigfiles:
                            output_files.append(filecandidate)

        return cli_command, output_files

    except subprocess.CalledProcessError as e:
        error_message = "Please take a screenshot of this error and raise an issue at the Bilayers repository on GitHub."
        error_message += f"Command failed with error: {e.stderr.decode()}\n\n"
        raise Exception(error_message)

st.session_state.done_running = os.path.exists("outputs.zip")

st.markdown(f"# Classical Segmentation - Brought to you in Streamlit by Bilayers")

st.markdown("""**This interface provides the following tool(s):**

Classical Segmentation: Segments images using classical thresholding methods : Otsu and Li

**This project relies on citations! Please cite ALL of the following if you find this application useful in your research:**

Cite Classical Segmentation using doi_number

**Licenses of the components:**

Classical Segmentation is provided under the license_details license

Bilayers is provided under the BSD 3-Clause license

Streamlit is provided under the Apache License 2.0 license""")

show_command = st.checkbox("Show command that Bilayers ran when reporting results (must be checked before hitting submit)")

show_file_list = st.checkbox("Show the list of files Bilayers is exporting when reporting results (must be checked before hitting submit)")

with st.form("my_form"): 


    inputs_dict = {}
    
    
    input_images_description = st.markdown("Upload all images to be analyzed")
    input_images = st.file_uploader(label="Drag and drop all images to be analyzed", accept_multiple_files=True)
    inputs_dict["input_images"]={"folder_name":"/bilayers/input_images","file_list":input_images}
    


    

    

    

    
    options_list_threshold_method = ["otsu", "li"]
    options_list_threshold_method_values = ["otsu", "li"]
    default_index_threshold_method = options_list_threshold_method_values.index("otsu")
    
    threshold_method = st.radio(label="Select a Threshold Method", help="Select a threshold method to segment the image", options=options_list_threshold_method, index=default_index_threshold_method)
    

    

    

    
    min_diameter = st.number_input(label="Object Minimum Diameter Size", help="Minimum diameter of objects in pixels", value=5 if "float" == "integer" else 5)
    

    

    

    
    max_diameter = st.number_input(label="Object Maximum Diameter Size", help="Maximum diameter of objects in pixels", value=20 if "float" == "integer" else 20)
    

    

    

    
    save_dir = st.text_input(label="Save Directory", help="directory to save output files", value="/bilayers/output_images") 
    

    

    
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        #we need to download the files to local disk - yuck!
        for k,v in inputs_dict.items():
            thisinput_list = v["file_list"]
            if len(thisinput_list) > 0:
                thisinput_location = v["folder_name"]
                if not os.path.exists(thisinput_location):
                    os.makedirs(thisinput_location,exist_ok=True)
                for eachfile in thisinput_list:
                    local_name = os.path.join(thisinput_location,eachfile.name)
                    with open(local_name,"wb") as f:
                        f.write(eachfile.getbuffer())
        with st.empty():
            try:
                with st.spinner("Processing, please wait",show_time=True):
                    cli_command_run, outputs = on_submit(
                        
                        input_images_description = input_images_description,
                        input_images = inputs_dict["input_images"]["folder_name"],
                        
                        threshold_method = threshold_method,min_diameter = min_diameter,max_diameter = max_diameter,save_dir = save_dir,
                        
                    )
                if show_command:
                    cmd_text = f"\n\nCommand run was `{cli_command_run}`"
                else:
                    cmd_text = ""
                if show_file_list:
                    file_text = "the following outputs for download:\n\n ```"+f','.join(outputs)+"``` \n\n"
                else:
                    file_text = "all outputs."
                st.markdown(f"Run complete, zipping {file_text}{cmd_text}")
                result = subprocess.run("python -m zipfile -c outputs.zip "+" ".join([x.replace(' ', '\ ') for x in outputs]), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                st.markdown(f"Results ready for download, zipped up {file_text}{cmd_text}")
                st.session_state.done_running = True
            
            except Exception as e:
                st.exception(e)

if st.session_state.done_running:
    with open("outputs.zip","rb") as file:
        st.download_button(label="Download results", data = file, file_name= "outputs.zip" )
        
