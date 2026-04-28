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
    DEPRECATED: Will be removed after repo extraction.
    Use installed package discovery instead.
    """
    import warnings

    warnings.warn(
        "project_path() is deprecated and will be removed after repo extraction. Use configuration-based discovery or entry points instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return (package_path() / "../..").resolve()
