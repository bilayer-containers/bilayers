"""
Shared utilities for interface generators.
"""

from bilayers_schema import Citations


def generate_top_level_text(interface_citation: Citations, citations: dict[str, Citations], output_html: bool = True) -> tuple[str, str]:
    """
    Generates a title and a full description (including tool, citation, and license information)
    based on the given interface type and citations.

    Args:
        interface_citation (Citations): The citation of the interface (e.g. "Gradio" or "Jupyter").
        citations (dict[str, Citations]): A dictionary of additional citations, where the key is a name of the tool/interface.
        output_html (bool): If True, use <br> as newline separator; otherwise use \n\n.

    Returns:
        tuple[str, str]: A title string and a full description string.
    """
    # Default citations for Interfaces and Bilayers
    BILAYERS: Citations = {
        "name": "Bilayers",
        "doi": "",
        "license": "BSD 3-Clause",
        "description": "A Container Specification and CI/CD built for whole-community support",
    }
    assert "name" in interface_citation and interface_citation.get("name"), "Must provide a name for interface citation"

    interface_name = interface_citation.get("name")

    newline = "<br>" if output_html else "\n\n"

    app_descriptions_lines = ["**This interface provides the following tool(s):**"]
    citation_text_lines = ["**This project relies on citations! Please cite ALL of the following if you find this application useful in your research:**"]
    license_info_lines = ["**Licenses of the components:**"]
    app_names_lines = []

    # Iterate through the citations dictionary from the config
    for name, citation in citations.items():
        app_descriptions_lines.append(f"{name}: {citation.get('description', '')}")
        if citation.get("doi"):
            citation_text_lines.append(f"Cite {name} using {citation.get('doi', 'N/A')}")
        license_info_lines.append(f"{name} is provided under the {citation.get('license', 'Unknown')} license")
        app_names_lines.append(name)

    # Add default citations for "Bilayers" and for the given interface
    for citation in [BILAYERS, interface_citation]:
        if citation.get("doi"):
            citation_text_lines.append(f"Cite {citation.get('name')} using {citation.get('doi', 'N/A')}")
        license_info_lines.append(f"{citation.get('name')} is provided under the {citation.get('license', 'Unknown')} license")

    title = "+".join(app_names_lines) + f" - Brought to you in {interface_name} by Bilayers"
    # Instead of joining with newlines, join with <br> so that the markdown cell shows line breaks
    full_description = f"{newline}".join(
        [f"{newline}".join(app_descriptions_lines), f"{newline}".join(citation_text_lines), f"{newline}".join(license_info_lines)]
    )

    return title, full_description
