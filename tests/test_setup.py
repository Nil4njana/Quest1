from pathlib import Path

from src.pipeline import PROJECT_ROOT


def test_project_root_exists():
    assert PROJECT_ROOT.exists()
    assert PROJECT_ROOT.is_dir()


def test_source_package_exists():
    source_dir = PROJECT_ROOT / "src"

    assert source_dir.exists()
    assert (source_dir / "__init__.py").exists()
    assert (source_dir / "pipeline.py").exists()