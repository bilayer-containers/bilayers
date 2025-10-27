from pathlib import Path
from typing import Optional, Any, Union
import json

from bilayers.parse import Citations, InputOutput, Parameter, ExecFunction


def _map_type_to_cytomine(param_type: str, param: Union[InputOutput, Parameter]) -> dict[str, Any]:
    """Map bilayers parameter types to Cytomine schema types."""
    if param_type == "integer":
        return {"id": "integer"}
    elif param_type == "float":
        return {"id": "number"}
    elif param_type == "boolean":
        return {"id": "boolean"}
    elif param_type == "textbox":
        return {"id": "string"}
    elif param_type in ["radio", "dropdown"]:
        options = param.get("options") or []
        values = [opt.get("value", opt.get("label", "")) for opt in options]
        return {"id": "enumeration", "values": values}
    elif param_type == "image":
        return {"id": "image"}
    elif param_type == "file":
        return {"id": "file"}
    elif param_type == "array":
        return {"id": "array", "subtype": {"id": "string"}}
    elif param_type == "measurement":
        return {"id": "file"}
    elif param_type == "executable":
        return {"id": "file"}
    else:
        return {"id": "string"}


def _convert_input_output(io_dict: dict[str, InputOutput], is_input: bool = True) -> dict[str, Any]:
    """Convert inputs or outputs to Cytomine schema format."""
    result = {}

    for name, io_param in io_dict.items():
        param_type = io_param.get("type", "string")
        type_spec = _map_type_to_cytomine(param_type, io_param)

        cytomine_param = {"description": io_param.get("description", ""), "type": type_spec}

        # Add display_name if label exists
        if "label" in io_param:
            cytomine_param["display_name"] = io_param["label"]

        # Add optional field for inputs
        if is_input and io_param.get("optional", False):
            cytomine_param["optional"] = True

        # Add default value for inputs with supported types
        if is_input and "default" in io_param:
            default_value = io_param["default"]
            if param_type in ["integer", "float", "boolean", "textbox"] and default_value is not None:
                cytomine_param["default"] = default_value

        result[name] = cytomine_param

    return result


def generate_cytomine(
    output_dir: Path,
    inputs: dict[str, InputOutput],
    outputs: dict[str, InputOutput],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
):
    # Create the Cytomine task schema
    task_schema = {
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "name": exec_function.get("name", "Algorithm Task"),
        "namespace": "bilayers.algorithm.task",
        "version": "1.0.0",
        "authors": [],
        "configuration": {"input_folder": "/inputs", "output_folder": "/outputs", "resources": {"ram": "1Gi", "gpus": 0, "cpus": 1, "internet": False}},
        "inputs": {},
        "outputs": {},
    }

    # Add description from citations if available
    if citations:
        first_citation = next(iter(citations.values()))
        if "description" in first_citation:
            task_schema["description"] = first_citation["description"]

    # Add authors from citations
    for citation in citations.values():
        # Create a basic author entry - this is simplified as citations don't contain full contact info
        author = {
            "first_name": "Algorithm",
            "last_name": "Author",
            "organization": "Unknown",
            "email": "unknown@example.com",
            "is_contact": len(task_schema["authors"]) == 0,  # First author is contact
        }
        task_schema["authors"].append(author)

    # If no citations, add a default author
    if not task_schema["authors"]:
        task_schema["authors"].append(
            {"first_name": "Algorithm", "last_name": "Author", "organization": "Unknown", "email": "unknown@example.com", "is_contact": True}
        )

    # Add external references from citations
    if citations:
        external = {}
        dois = []
        for citation in citations.values():
            if "doi" in citation and citation["doi"]:
                doi_url = citation["doi"]
                if not doi_url.startswith("http"):
                    doi_url = f"https://doi.org/{doi_url}"
                dois.append(doi_url)

        if dois:
            external["doi"] = dois
            task_schema["external"] = external

    # Convert inputs (includes parameters and display_only as inputs)
    all_inputs = {}
    all_inputs.update(inputs)

    # Add parameters as inputs
    for name, param in parameters.items():
        param_type = param.get("type", "string")
        type_spec = _map_type_to_cytomine(param_type, param)

        input_param = {"description": param.get("description", ""), "type": type_spec}

        if "label" in param:
            input_param["display_name"] = param["label"]

        if param.get("optional", False):
            input_param["optional"] = True

        if "default" in param and param["default"] is not None:
            input_param["default"] = param["default"]

        all_inputs[name] = input_param

    # Add display_only parameters as inputs
    if display_only:
        for name, param in display_only.items():
            param_type = param.get("type", "string")
            type_spec = _map_type_to_cytomine(param_type, param)

            input_param = {"description": param.get("description", ""), "type": type_spec}

            if "label" in param:
                input_param["display_name"] = param["label"]

            if "default" in param and param["default"] is not None:
                input_param["default"] = param["default"]

            all_inputs[name] = input_param

    task_schema["inputs"] = _convert_input_output(inputs, is_input=True)

    # Convert parameters to inputs in the schema
    for name, param in parameters.items():
        param_type = param.get("type", "string")
        type_spec = _map_type_to_cytomine(param_type, param)

        input_param = {"description": param.get("description", ""), "type": type_spec}

        if "label" in param:
            input_param["display_name"] = param["label"]

        if param.get("optional", False):
            input_param["optional"] = True

        if "default" in param and param["default"] is not None:
            input_param["default"] = param["default"]

        task_schema["inputs"][name] = input_param

    # Convert display_only to inputs
    if display_only:
        for name, param in display_only.items():
            param_type = param.get("type", "string")
            type_spec = _map_type_to_cytomine(param_type, param)

            input_param = {"description": param.get("description", ""), "type": type_spec}

            if "label" in param:
                input_param["display_name"] = param["label"]

            if "default" in param and param["default"] is not None:
                input_param["default"] = param["default"]

            task_schema["inputs"][name] = input_param

    # Convert outputs
    task_schema["outputs"] = _convert_input_output(outputs, is_input=False)

    # Write the task schema to a JSON file
    output_file = output_dir / "cytomine.json"
    with open(output_file, "w") as f:
        json.dump(task_schema, f, indent=2)

    return output_file

def generate(
    output_dir: Path,
    inputs: dict[str, InputOutput],
    outputs: dict[str, InputOutput],
    parameters: dict[str, Parameter],
    display_only: Optional[dict[str, Parameter]],
    exec_function: ExecFunction,
    citations: dict[str, Citations],
):
    output_file = generate_cytomine(output_dir, inputs, outputs, parameters, display_only, exec_function, citations)

    print(f"Cytomine task schema generated successfully at {output_file}!")
