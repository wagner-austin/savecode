"""
Unit tests for the GitStatusPlugin in savecode.
"""

from pathlib import Path
from typing import Any, Dict
from unittest.mock import patch

from savecode.plugins.git_status import GitStatusPlugin


def test_git_status_plugin_with_files() -> None:
    """Test that GitStatusPlugin correctly populates all_files."""
    root = Path("/fake/repo")
    files = [
        root / "file1.py",
        root / "file2.js",
        root / "file3.py",
    ]

    with (
        patch("savecode.plugins.git_status._git_root", return_value=root),
        patch("savecode.plugins.git_status._git_changed", return_value=files),
        patch("savecode.plugins.git_status.normalize_path", side_effect=lambda x: x),
        patch(
            "pathlib.Path.exists", return_value=True
        ),  # Mock to make paths pass the existence check
    ):
        plugin = GitStatusPlugin()
        context: Dict[str, Any] = {
            "cli_opts": {"git": True, "staged": False, "unstaged": False},
            "extensions": ["py", "js"],
            "errors": [],
        }
        plugin.run(context)

        assert "all_files" in context
        assert len(context["all_files"]) == 3
        assert str(root / "file1.py") in context["all_files"]
        assert str(root / "file2.js") in context["all_files"]
        assert str(root / "file3.py") in context["all_files"]


def test_git_status_plugin_with_all_ext_flag() -> None:
    """Test that GitStatusPlugin respects the all_ext flag."""
    root = Path("/fake/repo")
    files = [
        root / "file1.py",
        root / "file2.js",
        root / "file3.py",
        root / "file4.txt",  # This extension is not in the allowed list
        root / "file5.md",  # This extension is not in the allowed list
        root / "Makefile",  # No extension
    ]

    with (
        patch("savecode.plugins.git_status._git_root", return_value=root),
        patch("savecode.plugins.git_status._git_changed", return_value=files),
        patch("savecode.plugins.git_status.normalize_path", side_effect=lambda x: x),
        patch(
            "pathlib.Path.exists", return_value=True
        ),  # Mock to make paths pass the existence check
    ):
        plugin = GitStatusPlugin()

        # First test: without all_ext flag (should filter by extension)
        context: Dict[str, Any] = {
            "cli_opts": {"git": True, "all_ext": False},
            "extensions": ["py", "js"],
            "errors": [],
        }
        plugin.run(context)

        assert "all_files" in context
        assert len(context["all_files"]) == 3  # Only py and js files
        assert str(root / "file1.py") in context["all_files"]
        assert str(root / "file2.js") in context["all_files"]
        assert str(root / "file3.py") in context["all_files"]
        assert str(root / "file4.txt") not in context["all_files"]
        assert str(root / "file5.md") not in context["all_files"]
        assert str(root / "Makefile") not in context["all_files"]

        # Second test: with all_ext flag (should include all files)
        context = {
            "cli_opts": {"git": True, "all_ext": True},
            "extensions": ["py", "js"],
            "errors": [],
        }
        plugin.run(context)

        assert "all_files" in context
        assert len(context["all_files"]) == 6  # All files included
        assert str(root / "file1.py") in context["all_files"]
        assert str(root / "file2.js") in context["all_files"]
        assert str(root / "file3.py") in context["all_files"]
        assert str(root / "file4.txt") in context["all_files"]
        assert str(root / "file5.md") in context["all_files"]
        assert str(root / "Makefile") in context["all_files"]
