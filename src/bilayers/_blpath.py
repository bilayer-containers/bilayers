from pathlib import Path

from . import __path__


def package_path():
    """
    Returns an absolute path to the bilayers package (this one)
        /absolute/path/to/bilayers/src/bilayers/
    """
    return Path(__path__[0])


def project_path():
    """
    Returns an absolute path to the project dir hosting the bilayers package
        /absolute/path/to/bilayers/
    """
    return (package_path() / "../..").resolve()
