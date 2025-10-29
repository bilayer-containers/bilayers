"""Package source resolution utilities for materializing packages from various sources."""

import hashlib
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional


class SourceType(Enum):
    """Type of package source."""

    LOCAL = "local"
    PYPI = "pypi"
    GIT = "git"


@dataclass
class PackageSource:
    """Description of a package source."""

    source_type: SourceType
    location: str
    version: Optional[str] = None
    ref: Optional[str] = None  # For git sources

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result["source_type"] = self.source_type.value
        return result

    @classmethod
    def from_string(cls, source_str: str) -> "PackageSource":
        """
        Parse a source string into a PackageSource.

        Supported formats:
        - local:/path/to/package
        - pypi:package==version or pypi:package
        - git:https://github.com/user/repo@ref or git:https://github.com/user/repo

        Args:
            source_str: Source string to parse

        Returns:
            PackageSource instance

        Raises:
            ValueError: If the source string format is invalid
        """
        if source_str.startswith("local:"):
            location = source_str[6:]
            return cls(source_type=SourceType.LOCAL, location=location)

        elif source_str.startswith("pypi:"):
            package_spec = source_str[5:]
            if "==" in package_spec:
                location, version = package_spec.split("==", 1)
                return cls(source_type=SourceType.PYPI, location=location, version=version)
            else:
                return cls(source_type=SourceType.PYPI, location=package_spec)

        elif source_str.startswith("git:"):
            git_spec = source_str[4:]
            if "@" in git_spec:
                location, ref = git_spec.rsplit("@", 1)
                return cls(source_type=SourceType.GIT, location=location, ref=ref)
            else:
                return cls(source_type=SourceType.GIT, location=git_spec)

        else:
            raise ValueError(f"Invalid source format: {source_str}. Must start with local:, pypi:, or git:")

    def get_cache_key(self) -> str:
        """Generate a unique cache key for this source."""
        source_str = f"{self.source_type.value}:{self.location}"
        if self.version:
            source_str += f":{self.version}"
        if self.ref:
            source_str += f":{self.ref}"
        return hashlib.sha256(source_str.encode()).hexdigest()[:16]


class PackageResolver:
    """Resolves package sources and materializes them for introspection."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize the package resolver.

        Args:
            cache_dir: Directory for caching resolved packages. If None, uses system temp.
        """
        if cache_dir is None:
            cache_dir = Path(tempfile.gettempdir()) / "bilayers_package_cache"
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def resolve(self, source: PackageSource, force_refresh: bool = False) -> Path:
        """
        Resolve a package source to a local path.

        Args:
            source: Package source to resolve
            force_refresh: If True, ignore cache and re-download

        Returns:
            Path to the resolved package directory

        Raises:
            RuntimeError: If resolution fails
        """
        cache_key = source.get_cache_key()
        cache_path = self.cache_dir / cache_key

        # Check cache
        if cache_path.exists() and not force_refresh:
            metadata_path = cache_path / ".bilayers_metadata.json"
            if metadata_path.exists():
                return cache_path

        # Create cache directory
        cache_path.mkdir(parents=True, exist_ok=True)

        # Resolve based on source type
        if source.source_type == SourceType.LOCAL:
            self._resolve_local(source, cache_path)
        elif source.source_type == SourceType.PYPI:
            self._resolve_pypi(source, cache_path)
        elif source.source_type == SourceType.GIT:
            self._resolve_git(source, cache_path)

        # Save metadata
        self._save_metadata(source, cache_path)

        return cache_path

    def _resolve_local(self, source: PackageSource, target_path: Path) -> None:
        """Resolve a local package source."""
        source_path = Path(source.location).expanduser().resolve()

        if not source_path.exists():
            raise RuntimeError(f"Local package path does not exist: {source_path}")

        # Create a symlink to avoid copying large directories
        link_path = target_path / "package"
        if link_path.exists():
            link_path.unlink()
        link_path.symlink_to(source_path)

    def _resolve_pypi(self, source: PackageSource, target_path: Path) -> None:
        """Resolve a PyPI package source."""
        package_spec = source.location
        if source.version:
            package_spec += f"=={source.version}"

        # Download package using pip
        try:
            subprocess.run(
                [
                    "pip",
                    "download",
                    "--no-deps",
                    "--dest",
                    str(target_path),
                    package_spec,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to download PyPI package: {e.stderr}") from e

        # Install to a temporary location to make it importable
        install_path = target_path / "install"
        install_path.mkdir(exist_ok=True)

        try:
            subprocess.run(
                [
                    "pip",
                    "install",
                    "--no-deps",
                    "--target",
                    str(install_path),
                    package_spec,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install PyPI package: {e.stderr}") from e

    def _resolve_git(self, source: PackageSource, target_path: Path) -> None:
        """Resolve a Git repository source."""
        clone_path = target_path / "repo"

        # Clone repository
        try:
            cmd = ["git", "clone", source.location, str(clone_path)]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to clone git repository: {e.stderr}") from e

        # Checkout specific ref if provided
        if source.ref:
            try:
                subprocess.run(
                    ["git", "checkout", source.ref],
                    cwd=clone_path,
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to checkout git ref: {e.stderr}") from e

        # Install package in editable mode if setup.py/pyproject.toml exists
        if (clone_path / "pyproject.toml").exists() or (clone_path / "setup.py").exists():
            install_path = target_path / "install"
            install_path.mkdir(exist_ok=True)

            try:
                subprocess.run(
                    ["pip", "install", "--no-deps", "--target", str(install_path), str(clone_path)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to install git package: {e.stderr}") from e

    def _save_metadata(self, source: PackageSource, cache_path: Path) -> None:
        """Save source metadata to cache directory."""
        metadata = {
            "source": source.to_dict(),
            "resolved_at": str(Path.cwd()),
        }

        metadata_path = cache_path / ".bilayers_metadata.json"
        with metadata_path.open("w") as f:
            json.dump(metadata, f, indent=2)

    def get_import_path(self, resolved_path: Path) -> Path:
        """
        Get the path that should be added to sys.path for importing.

        Args:
            resolved_path: Path returned by resolve()

        Returns:
            Path to add to sys.path
        """
        # Check for install directory (PyPI/Git packages)
        install_path = resolved_path / "install"
        if install_path.exists():
            return install_path

        # Check for package symlink (local packages)
        package_link = resolved_path / "package"
        if package_link.exists():
            return package_link

        return resolved_path

    def generate_requirements(self, source: PackageSource, output_path: Path) -> None:
        """
        Generate a requirements.txt file for the package source.

        Args:
            source: Package source
            output_path: Path to write requirements.txt
        """
        lines = []

        if source.source_type == SourceType.LOCAL:
            # For local packages, reference the path
            lines.append(f"-e {source.location}")
        elif source.source_type == SourceType.PYPI:
            # For PyPI packages, use standard format
            package_spec = source.location
            if source.version:
                package_spec += f"=={source.version}"
            lines.append(package_spec)
        elif source.source_type == SourceType.GIT:
            # For git packages, use git+https format
            git_spec = f"git+{source.location}"
            if source.ref:
                git_spec += f"@{source.ref}"
            lines.append(git_spec)

        with output_path.open("w") as f:
            f.write("\n".join(lines) + "\n")

    def clear_cache(self) -> None:
        """Clear the package cache directory."""
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
