import os
import sys
from typing import Optional

# Importing parse function from parse.py
from parse import main as parse_config  # type: ignore
from jinja2 import Environment, FileSystemLoader, select_autoescape
import nbformat as nbf

# Import TypedDict definitions from parse.py
from parse import InputOutput, Parameter, ExecFunction, Citations, DockerImage  # type: ignore


def generate_top_level_text(interface: str, citations: dict[str, Citations], output_html: bool = True) -> tuple[str, str]:
    """
    Generates a title and a full description (including tool, citation, and license information)
    based on the given interface type and citations.

    Args:
        interface (str): The interface type (e.g. "Gradio" or "Jupyter").
        citations (dict[str, Citations]): A dictionary of citations, where the key is a name of the tool/interface.

    Returns:
        tuple[str, str]: A title string and a full description string.
    """
    # Default citations for Interfaces and Bilayers
    DEFAULT_CITATIONS: dict[str, Citations] = {
        "Bilayers": {
                "name": "Bilayers",
                "doi": "",
                "license": "BSD 3-Clause",
                "description": "A Container Specification and CI/CD built for whole-community support"
        },
        "Jupyter": {
                "name": "Jupyter",
                "doi": "10.1109/MCSE.2007.53",
                "license": "BSD 3-Clause",
                "description": "Interactive, code-driven documents for data analysis and visualization"
        },
        "Gradio": {
                "name": "Gradio",
                "doi": "10.48550/arXiv.190602569",
                "license": "Apache License 2.0",
                "description": "A simple web interface for deploying machine learning models"
        },
        "Streamlit": {
                "name": "Streamlit",
                "license": "Apache License 2.0",
                "description": "A library for easily creating custom web interfaces"
        },
    }

    newline = "<br>" if output_html else "\n\n"

    app_descriptions_lines = ["**This interface provides the following tool(s):**"]
    citation_text_lines = ["**This project relies on citations! Please cite ALL of the following if you find this application useful in your research:**"]
    license_info_lines = ["**Licenses of the components:**"]
    app_names_lines = []

    # Iterate through the citations dictionary from the config.
    for name, citation in citations.items():
        app_descriptions_lines.append(f"{name}: {citation.get('description', '')}")
        if citation.get("doi"):
            citation_text_lines.append(f"Cite {name} using {citation.get('doi', 'N/A')}")
        license_info_lines.append(f"{name} is provided under the {citation.get('license', 'Unknown')} license")
        app_names_lines.append(name)

    # Add default citations for "Bilayers" and for the given interface.
    for default_key in ["Bilayers", interface]:
        citation = DEFAULT_CITATIONS.get(default_key)
        if citation:
            if citation.get("doi"):
                citation_text_lines.append(f"Cite {citation.get('name', default_key)} using {citation.get('doi', 'N/A')}")
            license_info_lines.append(f"{citation.get('name', default_key)} is provided under the {citation.get('license', 'Unknown')} license")

    title = "+".join(app_names_lines) + f" - Brought to you in {interface} by Bilayers"
    # Instead of joining with newlines, join with <br> so that the markdown cell shows line breaks.
    full_description = f"{newline}".join([
        f"{newline}".join(app_descriptions_lines),
        f"{newline}".join(citation_text_lines),
        f"{newline}".join(license_info_lines)
    ])
    return title, full_description


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


def generate_gradio_app(
    template_path: str,
    inputs: dict[str, InputOutput],
    outputs: dict[str, InputOutput],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
) -> str:
    """
    Generates a Gradio application dynamically using Jinja2 templates.

    Args:
        template_path (str): Path to the Gradio template file.
        inputs (dict[str, InputOutput]): dictionary of input configurations.
        outputs (dict[str, InputOutput]): dictionary of output configurations.
        parameters (dict[str, Parameter]): dictionary of parameter configurations.
        display_only (Optional[dict[str, Parameter]]): dictionary of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (dict[str, Citations]): Citations information.

    Returns:
        str: The rendered Gradio application code.
    """
    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)), autoescape=select_autoescape(["j2"]))

    def lower(text: str) -> str:
        return text.lower()

    def replace(text: str, old: str, new: str) -> str:
        return text.replace(old, new)

    env.filters["lower"] = lower
    env.filters["replace"] = replace

    template = env.get_template(os.path.basename(template_path))

    title, full_description = generate_top_level_text('Gradio',citations, output_html=False)

    gradio_app_code: str = template.render(
        inputs=inputs, outputs=outputs, parameters=parameters, display_only=display_only, exec_function=exec_function, title=title, description=full_description
    )

    return gradio_app_code


def generate_jupyter_notebook(
    template_path: str,
    inputs: dict[str, InputOutput],
    outputs: dict[str, InputOutput],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
) -> nbf.NotebookNode:
    """
    Generates a Jupyter Notebook dynamically using Jinja2 templates.

    Args:
        template_path (str): Path to the Jupyter Notebook template file.
        inputs (dict[str, InputOutput]): dictionary of input configurations.
        outputs (dict[str, InputOutput]): dictionary of output configurations.
        parameters (dict[str, Parameter]): dictionary of parameter configurations.
        display_only (Optional[dict[str, Parameter]]): dictionary of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (dict[str, Citations]): Citations information.

    Returns:
        nbf.NotebookNode: The generated Jupyter Notebook object.
    """
    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)), autoescape=select_autoescape(["j2"]))

    def lower(text: str) -> str:
        return text.lower()

    def replace(text: str, old: str, new: str) -> str:
        return text.replace(old, new)

    def create_code_cell(content: str) -> nbf.NotebookNode:
        return nbf.v4.new_code_cell(content)

    def create_markdown_cell(content: str) -> nbf.NotebookNode:
        return nbf.v4.new_markdown_cell(content)

    template = env.get_template(os.path.basename(template_path))
    notebook_content: str = template.render(inputs=inputs, outputs=outputs, parameters=parameters, display_only=display_only, exec_function=exec_function)

    title, full_description = generate_top_level_text("Jupyter", citations, output_html=True)

    nb: nbf.NotebookNode = nbf.v4.new_notebook()

    # Add header markdown cells
    nb.cells.append(create_markdown_cell(f"# {title}"))
    nb.cells.append(create_markdown_cell(full_description))

    ########################################
    # Logic for Cell-1 in Jupyter Notebook
    ########################################
    # Create a hidden code cell for widget creation
    hidden_cell = create_code_cell(notebook_content)

    hidden_cell.metadata.jupyter = {"source_hidden": True}
    nb.cells.append(hidden_cell)

    ########################################
    # Logic for Cell-2 in Jupyter Notebook
    ########################################
    # Load and render the final validation template
    jupyter_final_validation_template_path = "jupyter_final_validation_template.py.j2"
    jupyter_final_validation_template = env.get_template(os.path.basename(jupyter_final_validation_template_path))
    final_validation_code = jupyter_final_validation_template.render()
    # final validation code cell
    final_validation_code_cell = create_code_cell(final_validation_code)
    final_validation_code_cell.metadata.jupyter = {"source_hidden": True}
    # Append a new code cell with the final validation code to the notebook
    nb.cells.append(final_validation_code_cell)

    ########################################
    # Logic for Cell-3 in Jupyter Notebook
    ########################################
    # jupyter_shell_command_template_path
    jupyter_shell_command_template_path = "jupyter_shell_command_template.py.j2"
    shell_command_template = env.get_template(os.path.basename(jupyter_shell_command_template_path))
    run_command_code: str = shell_command_template.render(cli_command=exec_function.get("cli_command", ""))
    # run command code cell
    run_command_code_cell = create_code_cell(run_command_code)
    run_command_code_cell.metadata.jupyter = {"source_hidden": True}
    # Append a new code cell with the run command code to the notebook
    nb.cells.append(run_command_code_cell)

    return nb

def generate_cellprofiler_plugin(
        template_path: str,
        inputs: dict[str, InputOutput],
        outputs: dict[str, InputOutput],
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
        template_path (str): Path to the CellProfiler Plugin template file.
        inputs (dict[str, InputOutput]): List of input configurations.
        outputs (dict[str, InputOutput]): List of output configurations.
        parameters (dict[str, Parameter]): List of parameter configurations.
        display_only (Optional[dict[str, Parameter]]): List of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (dict[str, Citations]): Citations information.

    Returns:
        .py file: The generated CellProfiler Plugin file.
    """
    env = Environment(
        loader=FileSystemLoader(searchpath=os.path.dirname(template_path)),
        autoescape=select_autoescape(['j2'])
    )
    
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

    template = env.get_template(os.path.basename(template_path))

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
        if paramvalue["type"] in ["float", "integer"] and paramvalue["default"] == "None":
            bool_param_dict = {k:v for k,v in paramvalue.items()}
            bool_param_dict["name"]=f"set_{paramkey}"
            bool_param_dict["type"]="radio"
            bool_param_dict["options"] = [{"label":"Yes","value":True},{"label":"No","value":False}]
            bool_param_dict["default"]="False"
            newlabel = paramvalue["label"][0].lower()+paramvalue["label"][1:]
            bool_param_dict["label"] = f"Set a value for {newlabel}?"
            num_param_dict = {k:v for k,v in paramvalue.items()}
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
        citations=citations,
        docker_image=docker_image
    )

    return cellprofiler_code, class_name

def generate_streamlit_app(
    template_path: str,
    inputs: dict[str, InputOutput],
    outputs: dict[str, InputOutput],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
) -> str:
    """
    Generates a Streamlit application dynamically using Jinja2 templates.

    Args:
        template_path (str): Path to the Streamlit template file.
        inputs (dict[str, InputOutput]): dictionary of input configurations.
        outputs (dict[str, InputOutput]): dictionary of output configurations.
        parameters (dict[str, Parameter]): dictionary of parameter configurations.
        display_only (Optional[dict[str, Parameter]]): dictionary of display-only parameters, or None.
        exec_function (ExecFunction): Execution function details.
        citations (dict[str, Citations]): Citations information.

    Returns:
        str: The rendered Streamlit application code.
    """
    env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)), autoescape=select_autoescape(["j2"]))

    def lower(text: str) -> str:
        return text.lower()

    def replace(text: str, old: str, new: str) -> str:
        return text.replace(old, new)

    env.filters["lower"] = lower
    env.filters["replace"] = replace

    template = env.get_template(os.path.basename(template_path))

    title, full_description = generate_top_level_text('Streamlit',citations, output_html=False)

    streamlit_app_code: str = template.render(
        inputs=inputs, outputs=outputs, parameters=parameters, display_only=display_only, exec_function=exec_function, title=title, description=full_description
    )

    return streamlit_app_code

def main() -> None:
    """Main function to parse config and generate Gradio and Jupyter notebook files."""
    print("Parsing config...")

    if len(sys.argv) > 1:
        config_path: Optional[str] = sys.argv[1]
    else:
        config_path = None

    inputs, outputs, parameters, display_only, exec_function, algorithm_folder_name, citations, docker_image = parse_config(config_path)

    folderA: str = "generated_folders"
    folderB: str = algorithm_folder_name
    # Create Directory if they don't exist
    os.makedirs(os.path.join(folderA, folderB), exist_ok=True)

    ########################################
    # Logic for generating Gradio App
    ########################################

    # Template path for the Gradio app
    gradio_template_path: str = "gradio_template.py.j2"

    # Generating the gradio algorithm+interface app dynamically
    gradio_app_code: str = generate_gradio_app(gradio_template_path, inputs, outputs, parameters, display_only, exec_function, citations)

    # Join folders and file name
    gradio_app_path: str = os.path.join(folderA, folderB, "app.py")

    # Generating Gradio app file dynamically
    with open(gradio_app_path, "w") as f:
        f.write(gradio_app_code)
    print("app.py generated successfully!!")

    ################################################
    # Logic for generating Jupyter Notebook
    ################################################

    # Template path for the Jupyter Notebook
    jupyter_template_path: str = "jupyter_template.py.j2"

    # Generating Jupyter Notebook file dynamically
    jupyter_app_code: nbf.NotebookNode = generate_jupyter_notebook(jupyter_template_path, inputs, outputs, parameters, display_only, exec_function, citations)

    # Join folders and file name
    jupyter_notebook_path: str = os.path.join(folderA, folderB, "generated_notebook.ipynb")

    with open(jupyter_notebook_path, "w") as f:
        nbf.write(jupyter_app_code, f)
    print("Jupyter notebook saved as generated_notebook.ipynb")

    ################################################
    # Logic for generating CellProfiler Plugin
    ################################################

    # Template path for the CellProfiler Plugin
    cellprofiler_plugin_template_path: str = "cellprofiler_plugin_template.py.j2"

    # Generating CellProfiler Plugin file dynamically
    cellprofiler_template_code: str
    plugin_name: str
    cellprofiler_template_code, plugin_name = generate_cellprofiler_plugin(
        cellprofiler_plugin_template_path,
        inputs,
        outputs,
        parameters,
        display_only,
        algorithm_folder_name,
        exec_function,
        citations,
        docker_image
    )

    # Join folders and file name - file name MUST match plugin name (but in lowercase) to work
    cellprofiler_plugin_path: str = os.path.join(folderA, folderB, f'{plugin_name.lower()}.py')

    # Generating CellProfiler Plugin file dynamically
    with open(cellprofiler_plugin_path, 'w') as f:
        f.write(cellprofiler_template_code)
    print("CellProfiler plugin generated successfully!!")
   
    ########################################
    # Logic for generating Streamlit App
    ########################################

    # Template path for the Streamlit app
    streamlit_template_path: str = "streamlit_template.py.j2"

    # Generating the gradio algorithm+interface app dynamically
    streamlit_app_code: str = generate_streamlit_app(streamlit_template_path, inputs, outputs, parameters, display_only, exec_function, citations)

    # Join folders and file name
    streamlit_app_path: str = os.path.join(folderA, folderB, "streamlit_app.py")

    # Generating Streamlit app file dynamically
    with open(streamlit_app_path, "w") as f:
        f.write(streamlit_app_code)
    print("streamlit_app.py generated successfully!!")

if __name__ == "__main__":
    main()
