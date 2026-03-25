####################################
# Auto-Generated CellProfiler Plugin
# Generated from Bilayers Spec File
####################################





#################################
#
# Imports from useful Python libraries
#
##################################

import os
import sys
import uuid
import shutil
import logging
import subprocess
import numpy
import skimage
import glob
import tempfile
import re

#################################
#
# Imports from CellProfiler
#
##################################





from cellprofiler_core.module.image_segmentation import ImageSegmentation, ObjectProcessing



from cellprofiler_core.module import ImageProcessing, Module



from cellprofiler_core.preferences import get_default_output_directory



from cellprofiler_core.object import Objects



from cellprofiler_core.setting import Binary



from cellprofiler_core.setting.subscriber import ImageSubscriber, LabelSubscriber



from cellprofiler_core.setting.text import ImageName, Integer, Float, Text, Directory, Filename, LabelName



from cellprofiler_core.setting.choice import Choice



from cellprofiler_core.image import Image



LOGGER = logging.getLogger(__name__)

__doc__ = f"""\
RunClassicalSegmentation
========================

**RunClassicalSegmentation** is an auto-generated CellProfiler module based on Bilayers specification.


This module processes input_images and produces segmented_images.


This module uses containers (Docker or Podman) to run the underlying algorithm, ensuring reproducible results 
across different systems. Make sure your chosen container runtime (Docker Desktop or Podman) is running before using this module.

|

============ ============ ===============
Supports 2D? Supports 3D? Respects masks?
============ ============ ===============
YES          YES          NO
============ ============ ===============

What do I need as input?
^^^^^^^^^^^^^^^^^^^^^^^^


- **Drag and drop all images to be analyzed**: Upload all images to be analyzed


What do I get as output?
^^^^^^^^^^^^^^^^^^^^^^^^


- **Segmented Images**: Segmented images




Technical notes
^^^^^^^^^^^^^^^

This module runs the classical_segmentation algorithm in a container (Docker or Podman).
The container image used is: bilayer/classical_segmentation:1.0.0


References
^^^^^^^^^^


- Classical Segmentation: Segments images using classical thresholding methods : Otsu and Li
  DOI: doi_number
  License: license_details


"""



class RunClassicalSegmentation(ImageSegmentation):
    #
    # The module starts by declaring the name that's used for display,
    # the category under which it is stored and the variable revision
    # number which can be used to provide backwards compatibility if
    # you add user-interface functionality later.
    #
    
    category = "Object Processing"
    
    
    module_name = "RunClassicalSegmentation"

    variable_revision_number = 1

    #
    # Citation - Please cite the following when using this module
    #
    
    doi = {
        
        "Please cite Classical Segmentation when using this module": "doi_number",
        
    }
    

    #
    # "create_settings" is where you declare the user interface elements
    # (the "settings") which the user will use to customize your module.
    #
    def create_settings(self):
        
         

        # Create input settings for all modules
        
        
        
        self.input_images = ImageSubscriber(
            "Drag and drop all images to be analyzed",
            doc="""\
Upload all images to be analyzed
"""
        )
        
        
        

        # Create output settings for all modules
        
        
        
        self.segmented_images = LabelName(
            "Segmented Images",
            "segmented_images",
            doc="""\
Segmented images
"""
        )
        
        
        

        #
        # Container Runner Selection - Choose how to execute the algorithm
        #
        self.execution_method = Choice(
            text="Execution method",
            
            choices=["Docker", "Podman"],
            value="Docker",
            doc="""\
Choose how to execute the algorithm:
- Docker: Run the algorithm in a Docker container (recommended for reproducibility)
- Podman: Run the algorithm in a Podman container (Docker alternative)
**Note**
- Python: "Future versions of this plugin may allow directly running in Python via a shared Python environment 
    - if so, those developers will add Python as an option here. If not added, only container-based run is supported."
"""
        )

        #
        # Container Image Selection - Works with both Docker and Podman
        #
        self.docker_image = Choice(
            text="Container image",
            choices=["bilayer/classical_segmentation:1.0.0"],
            value="bilayer/classical_segmentation:1.0.0",
            doc="""\
The container image to use for running this algorithm.
This works with both Docker and Podman container runtimes.
Make sure your chosen container runtime is installed and running.
The image will be automatically downloaded on first use.
"""
        )
        
        
        #
        # Select a Threshold Method
        #
        self.threshold_method = Choice(
            text="Select a Threshold Method",
            
            choices=[
                
                "otsu",
                
                "li",
                
            ],
            
            
            
            value="otsu",
            
            
            
            doc="""\
Select a threshold method to segment the image
"""
        )
        
        #
        # Object Minimum Diameter Size
        #
        self.min_diameter = Float(
            text="Object Minimum Diameter Size",
            
            
            
            value="5",
            
            
            
            minval=float('-inf'),
            maxval=float('inf'),
            
            doc="""\
Minimum diameter of objects in pixels
"""
        )
        
        #
        # Object Maximum Diameter Size
        #
        self.max_diameter = Float(
            text="Object Maximum Diameter Size",
            
            
            
            value="20",
            
            
            
            minval=float('-inf'),
            maxval=float('inf'),
            
            doc="""\
Maximum diameter of objects in pixels
"""
        )
        
        #
        # Save Directory
        #
        self.save_dir = Text(
            text="Save Directory",
            
            
            
            value="/bilayers/output_images",
            
            
            
            doc="""\
directory to save output files
"""
        )
        

        #
        # Clean up temporary files - Allow user to preserve temp files for debugging
        #
        self.clean_temp_files = Binary(
            text="Clean up temporary files",
            value=True,
            doc="""\
Select "Yes" to automatically delete temporary files after processing (recommended for normal use).
Select "No" to preserve temporary files for debugging purposes. The path to the temporary directory will be logged for manual inspection.
"""
        )

        
        
            
        
        

    #
    # The "settings" method tells CellProfiler about the settings you
    # have in your module. CellProfiler uses the list for saving
    # and restoring values for your module when it saves or loads a
    # pipeline file.
    #
    def settings(self):
        settings = []
        
        # All module settings - inputs, outputs, docker, and parameters
        
        settings.append(self.input_images)
        
        
        
        settings.append(self.segmented_images)
        
        
        
        
            
        
        
        
        # Docker and parameter settings
        settings.append(self.execution_method)
        settings.append(self.docker_image)
        settings.append(self.clean_temp_files)
        
        settings.append(self.threshold_method)
        
        settings.append(self.min_diameter)
        
        settings.append(self.max_diameter)
        
        settings.append(self.save_dir)
        
        
        return settings

    #
    # "visible_settings" tells CellProfiler which settings should be
    # displayed and in what order.
    #
    def visible_settings(self):
        visible = []
        
        # All module visible settings - inputs, outputs, docker, and parameters
        
        visible.append(self.input_images)
        
        
        
        visible.append(self.segmented_images)
        
        
        
        
        
            
        
        
        
        visible.append(self.execution_method)
        visible.append(self.docker_image)
        visible.append(self.clean_temp_files)
        
        
        visible.append(self.threshold_method)
        
        
        
        visible.append(self.min_diameter)
        
        
        
        visible.append(self.max_diameter)
        
        
        
        visible.append(self.save_dir)
        
        
        
        return visible

    #
    # CellProfiler calls "run" on each image set in your pipeline.
    # This is the core processing function that executes the algorithm.
    #
    def run(self, workspace):
        # Execute algorithm based on selected method
        execution_method = self.execution_method.value

        if execution_method in ["Docker", "Podman"]:
            # Container execution path
            self._run_container_execution(workspace)
        elif execution_method == "Python":
            # Python execution path (future feature)
            raise NotImplementedError("Local Python environment execution is not yet implemented. Please use Docker or Podman execution.")
        else:
            raise ValueError(f"Unknown execution method: {execution_method}")

    def _run_container_execution(self, workspace):
        """Execute the algorithm using Docker or Podman containers."""
        # Load input data and get names
        
        
        # Load image inputs
        
        
        input_images_name = self.input_images.value
        
        # Regular image input
        images = workspace.image_set
        input_images = images.get_image(input_images_name)
        input_images_data = input_images.pixel_data
        dimensions = input_images.dimensions
        
        
        
        
        
        # Load non-image inputs
        
        
        

        # Get output names
        
        
        segmented_images_name = self.segmented_images.value
        
        

        # Set up Docker/Podman's execution environment
        # Define how to call docker/podman
        if self.execution_method.value == "Docker":
            docker_path = "docker" if sys.platform.lower().startswith("win") else "/usr/local/bin/docker"
        elif self.execution_method.value == "Podman":
            docker_path = "podman" if sys.platform.lower().startswith("win") else "/opt/podman/bin/podman"

        # Create temporary directory (same as official CP modules)
        temp_dir = tempfile.mkdtemp(prefix=f"CP_{self.module_name}_")
        temp_input_dir = os.path.join(temp_dir, "input")
        temp_output_dir = os.path.join(temp_dir, "output")

        os.makedirs(temp_input_dir, exist_ok=True)
        os.makedirs(temp_output_dir, exist_ok=True)

        # =============================================================
        # Collect all input/output folder mounts dynamically 
        # Note: Don't keep inputs and outputs in the same mount to avoid conflicts
        # =============================================================
        mounts = []
        input_dirs = []
        output_dirs = []

        # ---- Handle INPUTS ----
        
        for key, inp in {"input_images": {"cli_order": 0, "cli_tag": "--folder", "default": "directory", "depth": True, "description": "Upload all images to be analyzed", "file_count": "multiple", "folder_name": "/bilayers/input_images", "format": ["tiff", "ometiff", "png", "jpg", "jpeg"], "label": "Drag and drop all images to be analyzed", "mode": "beginner", "name": "input_images", "optional": False, "pyramidal": True, "section_id": "inputs", "subtype": ["grayscale", "color", "binary"], "tiled": True, "timepoints": True, "type": "image", "unique_string": ["*"]}}.items():
            folder = inp.get("folder_name")
            cli_tag = inp.get("cli_tag")
            if folder:
                # Make a host-side path for this input
                host_subdir = os.path.join(temp_dir, "input", os.path.basename(folder.strip("/")))
                os.makedirs(host_subdir, exist_ok=True)
                mounts.append(("-v", f"{host_subdir}:{folder}"))
                input_dirs.append((cli_tag, folder))
            else:
                # Default fallback for missing folder_name
                folder = "/bilayers/input_images"
                host_subdir = os.path.join(temp_dir, "input", "input_images")
                os.makedirs(host_subdir, exist_ok=True)
                mounts.append(("-v", f"{host_subdir}:{folder}"))
                input_dirs.append((cli_tag, folder))

        # ---- Handle OUTPUTS ----
        
        for key, out in {"segmented_images": {"cli_order": 0, "cli_tag": "None", "default": "directory", "depth": True, "description": "Segmented images", "file_count": "single", "folder_name": "/bilayers/output_images", "format": ["tiff"], "label": "Segmented Images", "mode": "beginner", "name": "segmented_images", "optional": False, "pyramidal": True, "section_id": "outputs", "subtype": ["label"], "tiled": True, "timepoints": True, "type": "image", "unique_string": ["_output"]}}.items():
            folder = out.get("folder_name")
            cli_tag = out.get("cli_tag")
            if folder:
                if folder not in [x[1] for x in input_dirs]:
                    host_subdir = os.path.join(temp_dir, "output", os.path.basename(folder.strip("/")))
                    os.makedirs(host_subdir, exist_ok=True)
                    mounts.append(("-v", f"{host_subdir}:{folder}"))
                    output_dirs.append((cli_tag, folder))
                else:
                    # Some algorithms, like instanseg, use the input directory instead
                    host_subdir = os.path.join(temp_dir, "input", os.path.basename(folder.strip("/")))
                    output_dirs.append((cli_tag, folder))
                    temp_output_dir = temp_input_dir
            else:
                folder = "/bilayers/output"
                host_subdir = os.path.join(temp_dir, "output", "output")
                os.makedirs(host_subdir, exist_ok=True)
                mounts.append(("-v", f"{host_subdir}:{folder}"))
                output_dirs.append((cli_tag, folder))

        # ---- Also include global output_dir_set parameter if any ----
        
        for key, param in {"max_diameter": {"cli_tag": "--max_size", "default": 20, "description": "Maximum diameter of objects in pixels", "label": "Object Maximum Diameter Size", "mode": "beginner", "name": "max_diameter", "optional": False, "section_id": "input-args", "type": "float"}, "min_diameter": {"cli_tag": "--min_size", "default": 5, "description": "Minimum diameter of objects in pixels", "label": "Object Minimum Diameter Size", "mode": "beginner", "name": "min_diameter", "optional": False, "section_id": "input-args", "type": "float"}, "save_dir": {"cli_tag": "--save_dir", "default": "/bilayers/output_images", "description": "directory to save output files", "label": "Save Directory", "mode": "advanced", "name": "save_dir", "optional": True, "output_dir_set": True, "section_id": "output-args", "type": "textbox"}, "threshold_method": {"cli_tag": "--threshold_method", "default": "otsu", "description": "Select a threshold method to segment the image", "label": "Select a Threshold Method", "mode": "beginner", "name": "threshold_method", "optional": False, "options": [{"label": "otsu", "value": "otsu"}, {"label": "li", "value": "li"}], "section_id": "input-args", "type": "radio"}}.items():
            if param.get("output_dir_set"):
                cli_tag = param.get("cli_tag")
                val = getattr(self, param.get("name")).value if hasattr(self, param.get("name")) else param.get("default")
                if val:
                    host_subdir = os.path.join(temp_dir, "output", os.path.basename(val.strip("/")))
                    os.makedirs(host_subdir, exist_ok=True)
                    mounts.append(("-v", f"{host_subdir}:{val}"))
                    output_dirs.append((cli_tag, val))
        
        try:
            # ============================================================
            # Save input images inside the correct mounted input subfolder
            # ============================================================
            
            
            input_images_name = self.input_images.value
            image = workspace.image_set.get_image(input_images_name)
            input_images_data = image.pixel_data

            # Determine the correct subfolder (matches the Docker mount)
            folder_name = "/bilayers/input_images"
            host_input_subdir = os.path.join(temp_input_dir, os.path.basename(folder_name.strip("/")))
            os.makedirs(host_input_subdir, exist_ok=True)

            input_patterns = ["*"]
            saved = False

            for recognizer in input_patterns:
                if recognizer.strip() in ["*", "", None]:
                    continue
                safe_name = re.sub(r'[^A-Za-z0-9._-]', '_', recognizer)
                input_image_path = os.path.join(host_input_subdir, f"{safe_name}.tif")
                skimage.io.imsave(input_image_path, input_images_data)
                LOGGER.info(f"Saved input image to: {input_image_path}")
                saved = True
                break

            if not saved:
                # fallback: use sanitized logical name
                safe_name = re.sub(r'[^A-Za-z0-9._-]', '_', input_images_name)
                input_image_path = os.path.join(host_input_subdir, f"{safe_name}.tif")
                skimage.io.imsave(input_image_path, input_images_data)
                LOGGER.info(f"Saved input image (fallback) to: {input_image_path}")
            
            

            # Deduplicate volume mounts by target container path
            unique_mounts = []
            seen_targets = set()

            for flag, mapping in mounts:
                try:
                    target = mapping.split(":")[1]  # everything after the colon
                except IndexError:
                    target = mapping  # fallback, should never happen
                if target not in seen_targets:
                    seen_targets.add(target)
                    unique_mounts.append((flag, mapping))
                else:
                    LOGGER.debug(f"Skipping duplicate mount for target: {target}")

            mounts = unique_mounts
            LOGGER.info(f"Final unique mounts: {[m[1] for m in mounts]}")

            # Construct and execute Docker command
            cmd = [docker_path, "run", "--rm"]

            for flag, mapping in mounts:
                cmd.extend([flag, mapping])

            cmd.append(self.docker_image.value)
           
            
            
            cmd.append("python")
            
            cmd.append("-m")
            
            cmd.append("classical_segmentation")
            
            
            # Add input and parameter arguments
            for cli_tag, container_path in input_dirs:
                if cli_tag and container_path:
                    cmd.extend([cli_tag, container_path])
            
            
            
            
            
            cmd.extend(["--threshold_method", str(self.threshold_method.value)])
            
            
            
            
            
            
            
            cmd.extend(["--min_size", str(self.min_diameter.value)])
            
            
            
            
            
            
            
            cmd.extend(["--max_size", str(self.max_diameter.value)])
            
            
            
            
            
            
            
            cmd.extend(["--save_dir", str(self.save_dir.value)])
            
            
            
            


            LOGGER.info(f"Running Docker command: {' '.join(cmd)}")

            # Execute Docker/Podman container
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            
            if result.returncode != 0:
                LOGGER.error(f"Container execution failed: {result.stderr}")
                raise RuntimeError(f"Container execution failed: {result.stderr}")

            # Load output data
            try:
                # ============================================================
                # Load and register outputs programmatically
                # ============================================================
                LOGGER.info("Loading algorithm outputs from container run...")

                
                # --------------------------
                # Handle output: segmented_images
                # --------------------------
                output_type = "image"
                output_name = "segmented_images"
                output_subtype = "['label']"
                output_plurality =  "single"
                search_patterns = ["_output"]
                output_formats = ["tiff"]
                matched_files = []

                # unique_string : * --> act as wildcard for all formats
                for fmt in output_formats:
                    for recognizer in search_patterns:
                        # Skip meaningless wildcard-only patterns
                        if recognizer.strip() in ["*", "", None]:
                            pattern = os.path.join(temp_output_dir, f"*.{fmt}")
                        else:
                            pattern = os.path.join(temp_output_dir, "**", f"*{recognizer}*.{fmt}") # Recursive search
                        matched_files.extend(glob.glob(pattern, recursive=True))

                if not matched_files:
                    LOGGER.warning(f"No matching output found for {output_name}")
                else:
                    if output_type == "image":
                        # Load one or multiple images
                        if len(matched_files) == 1:
                            data = skimage.io.imread(matched_files[0])
                        else:
                            if output_plurality != "single":
                                data = [skimage.io.imread(f) for f in matched_files]
                            else:
                                import difflib
                                data = skimage.io.imread(difflib.get_close_matches(recognizer,matched_files,n=1,cutoff=0)[0])
                                LOGGER.warning(f"Multiple files matching unique string {recognizer} were found. We're using our best guess.")

                        # Register as Image or Object
                        if "label" in output_subtype.lower() or output_type == "object":
                            obj = Objects()
                            obj.segmented = data
                            
                            
                            obj.parent_image = input_images.parent_image
                            
                            workspace.object_set.add_objects(obj, output_name)
                        else:
                            image = Image(data)
                            
                            image.parent_image = input_images.parent_image
                            
                            workspace.image_set.add(output_name, image)
                        # FIX: Use setattr and add _data suffix for the display() function
                        setattr(workspace.display_data, f"{output_name}_data", data)

                    elif output_type == "array":
                        if len(matched_files) == 1:
                            data = numpy.load(matched_files[0])
                        else:
                            data = [numpy.load(f) for f in matched_files]
                        # FIX: Use setattr and add _data suffix for the display() function
                        setattr(workspace.display_data, f"{output_name}_data", data)

                    elif output_type == "measurement":
                        selected_file = matched_files[0]
                        if hasattr(self, "save_measurements") and self.save_measurements.value:
                            default_output_dir = get_default_output_directory()
                            if hasattr(self, "measurement_directory"):
                                if self.measurement_directory.dir_choice == "Default Output Folder":
                                    output_dir = default_output_dir
                                else:
                                    output_dir = self.measurement_directory.get_absolute_path(default_output_dir)
                            else:
                                output_dir = default_output_dir
                            measurement_dir = os.path.join(output_dir, "measurements", str(workspace.measurements.image_number))
                            os.makedirs(measurement_dir, exist_ok=True)
                            final_path = os.path.join(measurement_dir, os.path.basename(selected_file))
                            shutil.copy2(selected_file, final_path)
                            LOGGER.info(f"Saved measurement file for {output_name} at: {final_path}")
                            # FIX: Use setattr and add _data suffix for the display() function
                            setattr(workspace.display_data, f"{output_name}_data", final_path)
                        else:
                            # FIX: Use setattr and add _data suffix for the display() function
                            setattr(workspace.display_data, f"{output_name}_data", selected_file)
                    else:
                        LOGGER.warning(f"Unknown output type {output_type} for {output_name}")

                

            except FileNotFoundError as ex:
                LOGGER.error(f"Algorithm output files not found: {ex}")
                raise FileNotFoundError(f"I'm sorry, the classical_segmentation algorithm seems to have crashed and I'm not sure why, since it's running in its own container. Expected output files were not created. Please check the algorithm parameters and try again.")
            except Exception as ex:
                LOGGER.error(f"Error loading algorithm outputs: {ex}")
                raise RuntimeError(f"Failed to load algorithm outputs: {ex}")

        finally:
            # Clean up temp files (CellProfiler-style)
            if self.clean_temp_files.value:
                try:
                    shutil.rmtree(temp_dir)
                    LOGGER.info(f"Temporary directory cleaned up: {temp_dir}")
                except OSError as ex:
                    LOGGER.warning(f"Unable to delete temp directory {temp_dir}: {ex}")
            else:
                LOGGER.info(f"Preserving temporary files for debugging at: {temp_dir}")

        # Store measurement and array outputs in display data
        
        
        

        # Prepare display data for all modules
        if self.show_window:
            # Set dimensions (either from image inputs or default)
            if 'dimensions' in locals():
                workspace.display_data.dimensions = dimensions
            else:
                workspace.display_data.dimensions = 2  # Default to 2D
                
            
            
            workspace.display_data.input_images_data = input_images_data
            
            
            
            
            if 'segmented_images_data' in locals():
                workspace.display_data.segmented_images_data = segmented_images_data
            
            

    #
    # "display" lets you use matplotlib to display your results.
    # This method is called when the user requests to see the output.
    #
    def display(self, workspace, figure):
        """
        Display the results of the module processing.
        """
        # Programmatically determine what images to display
        displayable_images = []
        
        # Add all images from inputs/outputs for all categories
        
        
        if hasattr(workspace.display_data, 'input_images_data'):
            displayable_images.append(('input_images_data', 'Drag and drop all images to be analyzed', 'input'))
        
        
        
        
        
        if hasattr(workspace.display_data, 'segmented_images_data'):
            
            displayable_images.append(('segmented_images_data', 'Segmented Images', 'segmentation'))
            
        
        
        
        # Remove duplicates while preserving order (in case input/output data attributes overlap)
        seen = set()
        unique_images = []
        for img_data, title, img_type in displayable_images:
            if img_data not in seen:
                seen.add(img_data)
                unique_images.append((img_data, title, img_type))
        displayable_images = unique_images
        
        # Calculate optimal grid layout
        num_images = len(displayable_images)
        if num_images == 0:
            return  # Nothing to display
        
        # Smart grid calculation
        if num_images == 1:
            num_rows, num_cols = 1, 1
        elif num_images == 2:
            num_rows, num_cols = 1, 2
        elif num_images <= 4:
            num_rows, num_cols = 2, 2
        elif num_images <= 6:
            num_rows, num_cols = 2, 3
        elif num_images <= 9:
            num_rows, num_cols = 3, 3
        else:
            # For more than 9 images, use a wider layout
            num_cols = min(4, num_images)
            num_rows = (num_images + num_cols - 1) // num_cols
        
        figure.set_subplots(dimensions=workspace.display_data.dimensions, subplots=(num_rows, num_cols))
        
        # Display images in the calculated grid
        for idx, (img_data, title, img_type) in enumerate(displayable_images):
            row = idx // num_cols
            col = idx % num_cols
            
            image = getattr(workspace.display_data, img_data)
            
            if img_type == 'segmentation':
                figure.subplot_imshow_labels(
                    image=image,
                    sharexy=figure.subplot(0, 0) if idx > 0 else None,
                    title=title,
                    x=row,
                    y=col,
                )
            else:
                figure.subplot_imshow(
                    colormap="gray",
                    image=image,
                    sharexy=figure.subplot(0, 0) if idx > 0 else None,
                    title=title,
                    x=row,
                    y=col,
                )

    #
    # "volumetric" indicates whether or not this module supports 3D images.
    # Return True if the module can handle 3D data, False otherwise.
    #
    def volumetric(self):
        """Return True if this module supports 3D processing.
        This is determined by checking if any input images require depth support.
        """
        
        
        
        
        
        return False
        

    #
    # The "upgrade_settings" method allows for backwards compatibility
    # when you modify the module's interface.
    #
    def upgrade_settings(self, setting_values, variable_revision_number, module_name):
        """
        Upgrade settings from a previous version of the module.
        """
        return setting_values, variable_revision_number