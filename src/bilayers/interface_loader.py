class MissingInterfaceDependencyError(RuntimeError):
    """Raised when an interface is not available."""


class InterfaceLoader:
    """Adapter for the interface registry provided by bilayers-targets."""

    def __init__(self) -> None:
        from bilayers_targets import available_ifaces

        self._available_ifaces = available_ifaces

    def list_interfaces(self) -> list[str]:
        return sorted(self._available_ifaces)

    def load_module(self, interface_name: str):
        module = self._available_ifaces.get(interface_name)

        if module is None:
            raise MissingInterfaceDependencyError(f"Interface '{interface_name}' is not available. Install with: pip install bilayers[{interface_name}]")

        if not hasattr(module, "generate") or not callable(module.generate):
            raise AttributeError(f"Interface '{interface_name}' does not provide callable generate(interface_input)")

        return module
