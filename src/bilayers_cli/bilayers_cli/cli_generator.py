import sys
from typing import Any, Optional, Union
from src.bilayers.build.parse.parse import Config, HiddenArgs

def option_to_append(cli_tag: str, value: Any) -> str:
    """
    Formats CLI options for appending to the command.

    Args:
        cli_tag (str): CLI tag (e.g., "--option").
        value (Any): The value to append.

    Returns:
        str: The formatted CLI option.
    """
    # A protective layer not to append None values
    # But also, this edge case is taken care before calling insert_into_jagged_array function
    if value is None:
        return ""

    if cli_tag == "":
        return str(value)  # Append only the value
    elif "=" in cli_tag:
        return f"{cli_tag}{value}"
    return f"{cli_tag} {value}"  # Append cli_tag and value

def insert_into_jagged_array(
    jagged_array: list[Optional[list[str]]],
    cli_order: int,
    cli_tag: str,
    value: Any
) -> None:
    """
    Inserts CLI arguments into a structured array to maintain ordering.

    Args:
        jagged_array (list[Optional[list[str]]]): The structured array for CLI options.
        cli_order (int): The order in which arguments should appear.
        cli_tag (str): The CLI tag.
        value (Any): The value to append.
    """
    while len(jagged_array) <= abs(cli_order):
        jagged_array.append(None)

    if jagged_array[abs(cli_order)] is None:
        jagged_array[abs(cli_order)] = []

    result = option_to_append(cli_tag, value)
    jagged_array[abs(cli_order)].append(result) # pyright: ignore

def generate_cli_command(parsed_config: Config) -> list[str]:
    """
    Generates a CLI command dynamically based on a parsed Bilayers YAML configuration.

    Args:
        parsed_config (dict[str, Any]): Parsed Bilayers YAML configuration.

    Returns:
        list[str]: The generated CLI command as a list of arguments.
    """
    exec_function = parsed_config.get("exec_function", {})
    cli_command = [exec_function.get("cli_command", "").strip()]  # Ensure the first element is the command

    # Combine inputs and parameters into a single dictionary
    cli_tags = {**parsed_config.get("inputs", {}), **parsed_config.get("parameters", {})}

    jagged_positive_array = []
    jagged_negative_array = []

    # Step-1: Handle regular CLI Parameters i.e. inputs and parameters
    for key, param in cli_tags.items():
        param_type = param.get("type") # type would always be present
        cli_tag = param.get("cli_tag", "")
        default_value = param.get("default", None)
        cli_order = param.get("cli_order", 0)
        optional = param.get("optional", False)
        folder_name: Optional[str] = param.get("folder_name")

        if cli_order < 0:
            while len(jagged_negative_array) <= abs(cli_order):
                jagged_negative_array.append(None)

        while len(jagged_positive_array) <= cli_order:
            jagged_positive_array.append(None)

        if param_type == "checkbox":
            append_value: Optional[bool] = param.get("append_value", False)
            if append_value:
                insert_into_jagged_array(
                    jagged_negative_array if cli_order < 0 else jagged_positive_array,
                    cli_order, cli_tag, default_value
                )
            else:
                if default_value:
                    if cli_order < 0:
                        jagged_negative_array[abs(cli_order)] = jagged_negative_array[abs(cli_order)] or []
                        jagged_negative_array[abs(cli_order)].append(cli_tag)
                    else:
                        jagged_positive_array[cli_order] = jagged_positive_array[cli_order] or []
                        jagged_positive_array[cli_order].append(cli_tag)

        else:
            if param_type in {"image", "measurement", "file", "executable", "array"} and folder_name:
                default_value = folder_name

            if default_value is None and not optional:
                raise ValueError(f"Error: '{key}' is a required argument and must have a value!")

            # rest of the param_types would be handled here
            # ✅ Acceptable Cases:
            # - ("--option", "value")     → Passes (Valid CLI tag and value)
            # - ("", "value")             → Passes (Empty cli_tag but valid value) → Since in such cases, we only wish to append the value without cli_tag
            #
            # ❌ Skipped Cases:
            # - ("--option", "")          → Skipped (Empty value is not allowed)
            # - (None, "value")           → Skipped (cli_tag is None)
            # - ("--option", None)        → Skipped (Value is None)
            # - ("--option", "None")      → Skipped (Value is "None" as a string)
            # - ("None", "value")         → Skipped (cli_tag is "None" as a string)
            if cli_tag not in [None, "None"] and default_value not in [None, "None", ""]:
                insert_into_jagged_array(
                    jagged_negative_array if cli_order < 0 else jagged_positive_array, cli_order, cli_tag, default_value
                )

    # Step-2: Handle hidden arguments
    hidden_args: Optional[dict[str, HiddenArgs]] = exec_function.get("hidden_args", {})

    # Ignoring pyright error for hidden_args.values() as it will always be a valid dictionary, most of the times empty though
    for arg in hidden_args.values(): # pyright: ignore
        cli_tag = arg.get("cli_tag", "")
        value = arg.get("value", "")
        cli_order = arg.get("cli_order", 0)
        hidden_append_value : Optional[bool] = arg.get("append_value")

        if cli_order < 0:
            while len(jagged_negative_array) <= abs(cli_order):
                jagged_negative_array.append(None)

        while len(jagged_positive_array) <= cli_order:
            jagged_positive_array.append(None)

        if isinstance(value, bool):
            if hidden_append_value:
                insert_into_jagged_array(
                    jagged_negative_array if cli_order < 0 else jagged_positive_array, cli_order, cli_tag, value
                )
            else:
                if value:
                    if cli_order < 0:
                        jagged_negative_array[abs(cli_order)] = jagged_negative_array[abs(cli_order)] or []
                        jagged_negative_array[abs(cli_order)].append(cli_tag)
                    else:
                        jagged_positive_array[cli_order] = jagged_positive_array[cli_order] or []
                        jagged_positive_array[cli_order].append(cli_tag)

        else:
            insert_into_jagged_array(
                jagged_negative_array if cli_order < 0 else jagged_positive_array, cli_order, cli_tag, value
            )

    # Step-3: Merge Ordered CLI Arguments
    for index in range(1, len(jagged_positive_array)):
        if jagged_positive_array[index]:
            cli_command.extend(jagged_positive_array[index])

    if jagged_positive_array and jagged_positive_array[0]:
        cli_command.extend(jagged_positive_array[0])

    for index in range(len(jagged_negative_array) - 1, 0, -1):
        if jagged_negative_array[index]:
            cli_command.extend(jagged_negative_array[index])

    return cli_command

def main(parsed_config: Config, return_as_string: bool) -> Union[str, list[str]]:
    """
    Main entry point for generating the CLI command.

    Args:
        parsed_config (dict[str, Any]): Parsed Bilayers YAML configuration.
        return_as_string (bool): Whether to return the command as a string or list.

    Returns:
        Any: The CLI command as a string (for CLI usage) or a list (for library usage).
    """
    try:
        cli_command = generate_cli_command(parsed_config)

        if return_as_string:
            return " ".join(cli_command) # CLI Usage (string)
        return cli_command  # Library Usage (list)

    except ValueError as e:
        print(f"\n {e}\n")
        sys.exit(1)
