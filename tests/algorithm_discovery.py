"""Shared discovery of the algorithm configs shipped by bilayers_algorithms.

Imported by the integration tests that parametrize over every shipped algorithm,
so the notion of "all algorithms" (and which are excluded) is defined in exactly
one place.
"""

from importlib.resources import files

PKG = "bilayers_algorithms"

# example_algorithm is a fill-in-the-blanks template (docker_image / cli_command
# intentionally blank), not a deployable algorithm - excluded from these tests.
TEMPLATES = {"example_algorithm"}


def algorithm_names() -> list:
    root = files(PKG)
    return sorted(
        entry.name
        for entry in root.iterdir()
        if entry.is_dir() and entry.name != "__pycache__" and entry.name not in TEMPLATES and entry.joinpath("config.yaml").is_file()
    )


def config_resource(name: str):
    """importlib.resources Traversable for an algorithm's config.yaml."""
    return files(PKG).joinpath(name).joinpath("config.yaml")


ALGORITHMS = algorithm_names()
