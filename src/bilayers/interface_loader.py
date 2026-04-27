from importlib.metadata import entry_points

_GROUP = "bilayers.interfaces"


class MissingInterfaceDependencyError(RuntimeError):
    """Raised when an interface exists but cannot be imported due to missing optional dependencies."""

    pass


class InterfaceLoader:
    """Adapter for entry-point-based interface discovery and loading."""

    def __init__(self) -> None:
        # Retrieve all registered entry points
        discovered = entry_points()
        if hasattr(discovered, "select"):
            # Python 3.10+
            eps = discovered.select(group=_GROUP)
        else:
            # Python 3.9
            eps = discovered.get(_GROUP, [])
        self._entry_points = {ep.name: ep for ep in eps}

    def list_interfaces(self) -> list[str]:
        """Return all available interface names."""
        return sorted(self._entry_points)

    def load_generate(self, interface_name: str):
        """Load the generate() callable for a given interface via entry points."""

        ep = self._entry_points.get(interface_name)

        if ep is None:
            # Interface not registered (or corresponding extra not installed)
            raise FileNotFoundError(f"Interface '{interface_name}' not found. Install with: pip install bilayers[{interface_name}]")

        try:
            generate_fn = ep.load()
        except ImportError as exc:
            missing = getattr(exc, "name", None)
            detail = f" (missing dependency: '{missing}')" if missing else ""
            raise MissingInterfaceDependencyError(
                f"Interface '{interface_name}' could not be loaded{detail}. Install with: pip install bilayers[{interface_name}]"
            ) from exc

        # Safety check: entry point must resolve to a callable
        if not callable(generate_fn):
            raise AttributeError(f"Interface '{interface_name}' entry point does not resolve to a callable generate(interface_input) function")

        return generate_fn
