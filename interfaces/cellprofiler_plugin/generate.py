import os
from typing import Optional
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from bilayers import project_path
from bilayers.parse import Citations, Input, Output, Parameter, ExecFunction, DockerImage
from bilayers.generate import generate_top_level_text


# TODO: put in wiki to make publically available
# The sparse matrix is based on things discussed here: https://docs.google.com/spreadsheets/d/1e3JXcwdtaJLQrNQApg0mAXccvQhirWZw1pk11TjpiME/edit?gid=0#gid=0
def determine_category_from_matrix(inputs: dict, outputs: dict) -> str:
    """Return a high-level algorithm category based on input/output type combinations.

    This function (in future) may be reused beyond the CellProfiler plugin generator
    (e.g., documentation grouping, interface filtering).
    It deliberately allows categories like "Decoder"
    even if CellProfiler itself will later map that to an existing module
    classification.
    """

    TYPE_MAP = {
        "image": "image",
        "measurement": "measurement",
        "array": "measurement",
        "file": "measurement",
        "executable": "measurement",
    }

    CATEGORY_MATRIX = {
        ("image",): {
            ("image",): "Image Processing",
            ("object",): "Image Segmentation",
            ("measurement",): "Measurement",
            ("image", "object"): "Image Segmentation",
            ("image", "measurement"): "Image Processing",
            ("object", "measurement"): "Image Segmentation",
            ("image", "object", "measurement"): "Image Segmentation",
        },
        ("object",): {
            ("image",): "Object Processing",
            ("object",): "Object Processing",
            ("measurement",): "Measurement",
            ("image", "object"): "Object Processing",
            ("image", "measurement"): "Object Processing",
            ("object", "measurement"): "Object Processing",
            ("image", "object", "measurement"): "Object Processing",
        },
        ("measurement",): {
            ("image",): "Decoder",
            ("object",): "Decoder",
            ("measurement",): "Measurement",
            ("image", "object"): "Decoder",
            ("image", "measurement"): "Decoder",
            ("object", "measurement"): "Decoder",
            ("image", "object", "measurement"): "Decoder",
        },
        ("image", "object"): {
            ("image",): "Object Processing",
            ("object",): "Object Processing",
            ("measurement",): "Measurement",
            ("image", "object"): "Object Processing",
            ("image", "measurement"): "Object Processing",
            ("object", "measurement"): "Object Processing",
            ("image", "object", "measurement"): "Object Processing",
        },
        ("image", "measurement"): {
            ("image",): "Image Processing",
            ("object",): "Image Segmentation",
            ("measurement",): "Measurement",
            ("image", "object"): "Image Segmentation",
            ("image", "measurement"): "Image Processing",
            ("object", "measurement"): "Image Segmentation",
            ("image", "object", "measurement"): "Image Segmentation",
        },
        ("object", "measurement"): {
            ("image",): "Object Processing",
            ("object",): "Object Processing",
            ("measurement",): "Measurement",
            ("image", "object"): "Object Processing",
            ("image", "measurement"): "Object Processing",
            ("object", "measurement"): "Object Processing",
            ("image", "object", "measurement"): "Object Processing",
        },
        ("image", "object", "measurement"): {
            ("image",): "Object Processing",
            ("object",): "Object Processing",
            ("measurement",): "Measurement",
            ("image", "object"): "Object Processing",
            ("image", "measurement"): "Object Processing",
            ("object", "measurement"): "Object Processing",
            ("image", "object", "measurement"): "Object Processing",
        }
    }

    def normalize_types(conf_dict: dict) -> set:
        resolved = []
        for c in conf_dict.values():
            base_type = TYPE_MAP.get(c.get("type"), "custom")
            if base_type == "image" and c.get("subtype"):
                subtypes = c.get("subtype", [])
                if "labeled" in subtypes:
                    resolved.append("object")
                else:
                    resolved.append("image")
            else:
                resolved.append(base_type)
        return set(resolved)

    def find_matching_category(input_set: set, output_set: set) -> str:
        """
        Simple lookup that checks if input/output sets match any category combination
        """
        for input_tuple, output_dict in CATEGORY_MATRIX.items():
            if set(input_tuple) == input_set:
                for output_tuple, category in output_dict.items():
                    if set(output_tuple) == output_set:
                        return category

        # If no exact match is found, try subset matching (more permissive)
        for input_tuple, output_dict in CATEGORY_MATRIX.items():
            if set(input_tuple).issubset(input_set):
                for output_tuple, category in output_dict.items():
                    if set(output_tuple).issubset(output_set):
                        return category
        return "Custom"

    return find_matching_category(normalize_types(inputs), normalize_types(outputs))


def normalize_category_for_cellprofiler(category: str) -> str:
    """Map internal/general categories to ones CellProfiler recognizes.

    Currently we collapse "Decoder" to "Measurement" so the generated
    plugin fits within existing CP UI groupings. Additional mappings can
    be adjusted here without touching the matrix logic.
    """
    if category == "Decoder":
        return "Not Supported"
    return category


def generate_cellprofiler_plugin(
        template_dir: Path,
        template_name: str,
        inputs: dict[str, Input],
        outputs: dict[str, Output],
        parameters: dict[str, Parameter],
        display_only: Optional[dict[str, Parameter]],
        algorithm_folder_name: str,
        exec_function: ExecFunction,
        citations: dict[str, Citations],
        docker_image: DockerImage
    ):
    """
    Generates a CellProfiler Plugin dynamically using Jinja2 templates.

    Args:
        template_dir (Path): Path to the Gradio template file's containing dir.
        template_name (str): name of the Gradio template file.
        inputs (dict[str, Input]): List of input configurations.
        outputs (dict[str, Output]): List of output configurations.
        parameters (dict[str, Parameter]): List of parameter configurations.
        display_only (Optional[dict[str, Parameter]]): List of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (dict[str, Citations]): Citations information.

    Returns:
        .py file: The generated CellProfiler Plugin file.
    """
    env = Environment(loader=FileSystemLoader(searchpath=str(template_dir)), autoescape=select_autoescape(["j2"]))

    # Helper function to convert algorithm folder name to class name
    def convert_to_class_name(algorithm_folder_name: str) -> str:
        """ Converts the algorithm folder name to a class name by adding run and converting to CamaelCase
        """
        camel_case = ''.join([x.capitalize() for x in algorithm_folder_name.split('_')])
        return "Run" + camel_case

    def lower(text: str) -> str:
        return text.lower()

    def replace(text: str, old: str, new: str) -> str:
        return text.replace(old, new)

    env.filters['lower'] = lower
    env.filters['replace'] = replace

    template = env.get_template(template_name)

    # Precompute the category, then normalize it for CellProfiler usage
    general_category = determine_category_from_matrix(inputs, outputs)
    computed_category = normalize_category_for_cellprofiler(general_category)

    # Abort generation if the category is explicitly not supported for CellProfiler
    if computed_category == "Not Supported":
        raise RuntimeError(
            "CellProfiler plugin generation aborted: general category 'Decoder' is not supported as a CellProfiler module. "
            "(We retain it for documentation / other interfaces.)"
        )

    # Convert algorithm folder name to class name
    class_name: str = convert_to_class_name(algorithm_folder_name)

    # Some parameters are numeric but have a default of None, because sometimes they aren't set. Ick!
    # Let's handle them by making a "set_x" setting, and a "value_x" setting, which is not visible if set_x is False
    split_parameters = {}
    parameters_flat = {}
    for paramkey, paramvalue in parameters.items():
        assert "type" in paramvalue and "default" in paramvalue and "label" in paramvalue
        if paramvalue["type"] in ["float", "integer"] and paramvalue["default"] == "None":
            bool_param_dict = dict(paramvalue)
            bool_param_dict["name"]=f"set_{paramkey}"
            bool_param_dict["type"]="radio"
            bool_param_dict["options"] = [{"label":"Yes","value":True},{"label":"No","value":False}]
            bool_param_dict["default"]="False"
            newlabel = paramvalue["label"][0].lower()+paramvalue["label"][1:]
            bool_param_dict["label"] = f"Set a value for {newlabel}?"
            num_param_dict = dict(paramvalue)
            num_param_dict["name"]=f"val_{paramkey}"
            num_param_dict["default"]=0
            split_parameters[paramkey]={f"set_{paramkey}":bool_param_dict,f"val_{paramkey}":num_param_dict}
            parameters_flat[f"set_{paramkey}"]=bool_param_dict
            parameters_flat[f"val_{paramkey}"]=num_param_dict
        else:
            parameters_flat[paramkey]=paramvalue


    cellprofiler_code: str = template.render(
        inputs=inputs,
        outputs=outputs,
        computed_category=computed_category,
        parameters=parameters_flat,
        split_parameters=split_parameters,
        display_only=display_only or [],
        algorithm_folder_name=class_name,
        exec_function=exec_function,
        # TODO: call generate_top_level_text or include the BILAYERS citation defined there
        citations=citations,
        docker_image=docker_image
    )

    return cellprofiler_code, class_name

def generate(
    output_dir: Path,
    inputs: dict[str, Input],
    outputs: dict[str, Output],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
    docker_image: DockerImage,
):
    cellprofiler_template_path = project_path() / "interfaces/cellprofiler_plugin"

    cellprofiler_plugin_code, plugin_name = generate_cellprofiler_plugin(
        cellprofiler_template_path,
        "cellprofiler_plugin_template.py.j2",
        inputs,
        outputs,
        parameters,
        display_only,
        output_dir.stem,
        exec_function,
        citations,
        docker_image)

    # join folders and file name - file name MUST match plugin name (but in lowercase) to work
    cellprofiler_plugin_path = output_dir / f"{plugin_name.lower()}.py"

    with open(cellprofiler_plugin_path, "w") as f:
        f.write(cellprofiler_plugin_code)

    print("CellProfiler plugin generated successfully!!")
