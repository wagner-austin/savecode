"""
Unit tests for the GitStatusPlugin in savecode.
"""

import sys
import pytest
import subprocess
from pathlib import Path
from unittest.mock import patch

from savecode.plugins.git_status import _git_root, _git_changed, GitStatusPlugin


def test_git_root_found(tmp_path):
    """Test that _git_root returns the correct path when in a git repository."""
    with patch("subprocess.check_output") as mock_output:
        mock_output.return_value = str(tmp_path) + "\n"
        result = _git_root(tmp_path)
        assert result == tmp_path
        mock_output.assert_called_once()


def test_git_root_not_found(tmp_path):
    """Test that _git_root returns None when not in a git repository."""
    with patch("subprocess.check_output") as mock_output:
        mock_output.side_effect = subprocess.CalledProcessError(1, "git")
        result = _git_root(tmp_path)
        assert result is None
        mock_output.assert_called_once()


def test_git_changed(tmp_path):
    """Test that _git_changed returns the correct list of files."""
    mock_output = """M  staged_modified.py
 M unstaged_modified.py
?? untracked.py
"""
    with patch("subprocess.check_output", return_value=mock_output):
        # Test both staged and unstaged
        result = _git_changed(tmp_path, True, True)
        assert len(result) == 3
        assert tmp_path / "staged_modified.py" in result
        assert tmp_path / "unstaged_modified.py" in result
        assert tmp_path / "untracked.py" in result

        # Test only staged
        with patch("subprocess.check_output", return_value="M  staged_modified.py\n"):
            result = _git_changed(tmp_path, True, False)
            assert len(result) == 1
            assert tmp_path / "staged_modified.py" in result

        # Test only unstaged
        result = _git_changed(tmp_path, False, True)
        assert len(result) == 2
        assert tmp_path / "unstaged_modified.py" in result
        assert tmp_path / "untracked.py" in result


def test_git_status_plugin_no_flag():
    """Test that GitStatusPlugin does nothing when --git is not set."""
    plugin = GitStatusPlugin()
    context = {"cli_opts": {"git": False}}
    plugin.run(context)
    assert "all_files" not in context


def test_git_status_plugin_not_in_repo():
    """Test that GitStatusPlugin handles not being in a git repository gracefully."""
    with patch("savecode.plugins.git_status._git_root", return_value=None):
        plugin = GitStatusPlugin()
        context = {"cli_opts": {"git": True}, "errors": []}
        plugin.run(context)
        assert len(context["errors"]) == 1
        assert "Not inside a Git repository" in context["errors"][0]


def test_git_status_plugin_with_files():
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
    ):
        plugin = GitStatusPlugin()
        context = {
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


def test_git_flag_integration(monkeypatch, tmp_path):
    """Integration test for the --git flag."""
    # create a fake repo with one modified file
    js_file = tmp_path / "file.js"
    js_file.write_text("foo")

    subprocess.run(["git", "-C", str(tmp_path), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "file.js"], check=True)
    js_file.write_text("bar")  # unstaged change

    # simulate CLI
    argv = ["savecode", "--git", "--ext", "js"]
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", argv)
        from savecode.cli import main

        with patch("builtins.print"):  # suppress output
            main()
