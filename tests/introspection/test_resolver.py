"""Tests for the package resolver module."""

import tempfile
from pathlib import Path
import pytest

from bilayers.introspection.resolver import PackageSource, PackageResolver, SourceType


def test_package_source_from_string_local():
    """Test parsing local package source string."""
    source = PackageSource.from_string("local:/path/to/package")

    assert source.source_type == SourceType.LOCAL
    assert source.location == "/path/to/package"
    assert source.version is None
    assert source.ref is None


def test_package_source_from_string_pypi():
    """Test parsing PyPI package source string."""
    source = PackageSource.from_string("pypi:numpy==1.24.0")

    assert source.source_type == SourceType.PYPI
    assert source.location == "numpy"
    assert source.version == "1.24.0"
    assert source.ref is None


def test_package_source_from_string_pypi_no_version():
    """Test parsing PyPI package source without version."""
    source = PackageSource.from_string("pypi:numpy")

    assert source.source_type == SourceType.PYPI
    assert source.location == "numpy"
    assert source.version is None


def test_package_source_from_string_git():
    """Test parsing Git package source string."""
    source = PackageSource.from_string("git:https://github.com/user/repo@main")

    assert source.source_type == SourceType.GIT
    assert source.location == "https://github.com/user/repo"
    assert source.ref == "main"


def test_package_source_from_string_git_no_ref():
    """Test parsing Git package source without ref."""
    source = PackageSource.from_string("git:https://github.com/user/repo")

    assert source.source_type == SourceType.GIT
    assert source.location == "https://github.com/user/repo"
    assert source.ref is None


def test_package_source_from_string_invalid():
    """Test that invalid source strings raise ValueError."""
    with pytest.raises(ValueError):
        PackageSource.from_string("invalid:source")

    with pytest.raises(ValueError):
        PackageSource.from_string("just_a_string")


def test_package_source_cache_key():
    """Test cache key generation."""
    source1 = PackageSource.from_string("pypi:numpy==1.24.0")
    source2 = PackageSource.from_string("pypi:numpy==1.24.0")
    source3 = PackageSource.from_string("pypi:numpy==1.25.0")

    # Same sources should have same cache key
    assert source1.get_cache_key() == source2.get_cache_key()

    # Different sources should have different cache keys
    assert source1.get_cache_key() != source3.get_cache_key()


def test_package_source_to_dict():
    """Test serializing PackageSource to dict."""
    source = PackageSource.from_string("pypi:numpy==1.24.0")
    data = source.to_dict()

    assert isinstance(data, dict)
    assert data["source_type"] == "pypi"
    assert data["location"] == "numpy"
    assert data["version"] == "1.24.0"


def test_package_resolver_init():
    """Test PackageResolver initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_dir = Path(tmpdir) / "cache"
        resolver = PackageResolver(cache_dir=cache_dir)

        assert resolver.cache_dir == cache_dir
        assert cache_dir.exists()


def test_package_resolver_resolve_local(tmp_path):
    """Test resolving a local package."""
    # Create a dummy local package
    local_package = tmp_path / "my_package"
    local_package.mkdir()
    (local_package / "__init__.py").write_text("# My package")

    # Create resolver
    cache_dir = tmp_path / "cache"
    resolver = PackageResolver(cache_dir=cache_dir)

    # Resolve
    source = PackageSource.from_string(f"local:{local_package}")
    resolved_path = resolver.resolve(source)

    assert resolved_path.exists()

    # Check symlink was created
    import_path = resolver.get_import_path(resolved_path)
    assert import_path.exists()


def test_package_resolver_clear_cache():
    """Test clearing the package cache."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_dir = Path(tmpdir) / "cache"
        resolver = PackageResolver(cache_dir=cache_dir)

        # Cache should be created
        assert cache_dir.exists()

        # Create some dummy content
        (cache_dir / "dummy.txt").write_text("test")

        # Clear cache
        resolver.clear_cache()

        # Cache directory should exist but be empty
        assert cache_dir.exists()
        assert len(list(cache_dir.iterdir())) == 0


def test_generate_requirements_pypi(tmp_path):
    """Test generating requirements.txt for PyPI package."""
    resolver = PackageResolver()
    source = PackageSource.from_string("pypi:numpy==1.24.0")

    output_file = tmp_path / "requirements.txt"
    resolver.generate_requirements(source, output_file)

    content = output_file.read_text()
    assert "numpy==1.24.0" in content


def test_generate_requirements_local(tmp_path):
    """Test generating requirements.txt for local package."""
    resolver = PackageResolver()
    source = PackageSource.from_string("local:/path/to/package")

    output_file = tmp_path / "requirements.txt"
    resolver.generate_requirements(source, output_file)

    content = output_file.read_text()
    assert "-e /path/to/package" in content


def test_generate_requirements_git(tmp_path):
    """Test generating requirements.txt for Git package."""
    resolver = PackageResolver()
    source = PackageSource.from_string("git:https://github.com/user/repo@main")

    output_file = tmp_path / "requirements.txt"
    resolver.generate_requirements(source, output_file)

    content = output_file.read_text()
    assert "git+https://github.com/user/repo@main" in content
