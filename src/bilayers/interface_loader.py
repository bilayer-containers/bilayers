import importlib.util
from pathlib import Path
from types import ModuleType


class MissingInterfaceDependencyError(RuntimeError):
    """Raised when an interface module cannot be imported because an optional dependency is missing."""


class InterfaceLoader:
    """Thin adapter for filesystem-based interface discovery and loading"""

    def __init__(self, interfaces_dir: Path) -> None:
        self.interfaces_dir = interfaces_dir

    def list_interfaces(self) -> list[str]:
        names = []
        for iface_dir in self.interfaces_dir.iterdir():
            if not iface_dir.is_dir() or iface_dir.name == "generated_folders":
                continue

            generate_py = iface_dir / "generate.py"
            if generate_py.exists():
                names.append(iface_dir.name)

        return names

    def get_generate_path(self, interface_name: str) -> Path:
        generate_py = self.interfaces_dir / interface_name / "generate.py"
        if not generate_py.exists():
            raise FileNotFoundError(f"Interface '{interface_name}' not found. Install with: pip install bilayers[{interface_name}]")
        return generate_py

    def load_module(self, interface_name: str) -> ModuleType:
        generate_py = self.get_generate_path(interface_name).resolve()

        spec = importlib.util.spec_from_file_location(
            f"bilayers_interface_{interface_name}",
            generate_py,
        )
        if not spec or not spec.loader:
            raise RuntimeError(f"Cannot load interface module for {interface_name}")

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except ImportError as exc:
            missing = getattr(exc, "name", None)
            detail = f" (missing dependency: '{missing}')" if missing else ""
            raise MissingInterfaceDependencyError(
                f"Interface '{interface_name}' could not be loaded{detail}. Install with: pip install bilayers[{interface_name}]"
            ) from exc

        if not hasattr(module, "generate") or not callable(module.generate):
            raise AttributeError(f"Interface '{interface_name}' doesn't have a callable generate(interface_input) function")
        return module
