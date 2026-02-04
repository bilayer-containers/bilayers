from typing import Any, Optional, Union

from .parse import Config, build_cli_sequence


def _option_to_append(cli_tag: str, value: Any) -> str:
    """
    Formats CLI options for appending to the command.

    Args:
        cli_tag (str): CLI tag (e.g., "--option").
        value (Any): The value to append.

    Returns:
        str: The formatted CLI option.
    """
    # A protective layer not to append None values
    # But also, this edge case is taken care before calling _insert_into_jagged_array function
    if value is None:
        return ""

    if cli_tag == "":
        return str(value)  # Append only the value
    elif "=" in cli_tag:
        return f"{cli_tag}{value}"
    return f"{cli_tag} {value}"  # Append cli_tag and value


def _generate_cli_command(parsed_config: Config) -> list[str]:  # noqa: C901
    """
    Generates a CLI command dynamically based on a parsed Bilayers YAML configuration.

    Args:
        parsed_config (dict[str, Any]): Parsed Bilayers YAML configuration.

    Returns:
        list[str]: The generated CLI command as a list of arguments.
    """
    exec_function = parsed_config.get("exec_function", {})
    cli_command = [exec_function.get("cli_command", "").strip()]  # Ensure the first element is the command

    cli_sequence = build_cli_sequence(parsed_config)

    for name, item in cli_sequence.items():
        source = item.get("source")
        cli_tag = item.get("cli_tag", "")
        param_type = item.get("type")
        optional = item.get("optional", False)

        if source == "hidden":
            value = item.get("value", "")
            append_value = item.get("append_value", False)
        else:
            value = item.get("default", None)
            append_value = item.get("append_value", False)
            folder_name: Optional[str] = item.get("folder_name")
            if param_type in {"image", "measurement", "file", "executable", "array"} and folder_name:
                value = folder_name

        if param_type == "checkbox" or isinstance(value, bool):
            if append_value:
                if cli_tag not in [None, "None"]:
                    cli_command.append(_option_to_append(cli_tag, value))
            else:
                if value and cli_tag not in [None, "None"]:
                    cli_command.append(cli_tag)
            continue

        if value is None and not optional:
            raise ValueError(f"Error: '{name}' is a required argument and must have a value!")

        if cli_tag not in [None, "None"] and value not in [None, "None", ""]:
            cli_command.append(_option_to_append(cli_tag, value))

    return cli_command


def generate_cli_command(parsed_config: Config, return_as_string: bool = False) -> Union[str, list[str]]:
    """
    Main entry point for generating the CLI command.

    Args:
        parsed_config (dict[str, Any]): Parsed Bilayers YAML configuration.
        return_as_string (bool): Whether to return the command as a string or list.

    Returns:
        Any: The CLI command as a string (for CLI usage) or a list (for library usage).
    """
    cli_command = _generate_cli_command(parsed_config)

    if return_as_string:
        return " ".join(cli_command)  # CLI Usage (string)
    return cli_command  # Library Usage (list)
