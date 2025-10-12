from pathlib import Path
from .cli_generator import generate_cli_command

__all__ = ["generate_cli_command", "package_path", "project_path"]

def package_path():
    """
    Returns an absolute path to the bilayers_cli package (this one)
        /absolute/path/to/bilayers_project/src/bilayers_cli/
    """
    return Path(__path__[0])

def project_path():
    """
    Returns an absolute path to the project dir hosting the bilayers_cli package
        /absolute/path/to/bilayers_project/
    """
    return (package_path() / '../..').resolve()
