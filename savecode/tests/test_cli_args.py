"""
savecode/tests/test_cli_args.py - Module for testing CLI argument parsing and skip functionality.
This module tests the new positional argument handling for source inputs, merging of -r and -f arguments,
and the robustness of --skip functionality.
"""

import os
import sys
import tempfile
import unittest
from savecode.utils.cli_args import parse_arguments
from savecode.plugins.gather import should_skip

class TestCLIArgs(unittest.TestCase):
    def test_positional_source_directory(self):
        """
        Test that a positional source directory is correctly added to roots.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            orig_argv = sys.argv
            sys.argv = ["prog", tmpdir]
            args, extra = parse_arguments()
            # Normalize and check that the temp directory is in roots.
            norm_roots = [os.path.normpath(os.path.abspath(x)) for x in args.roots]
            norm_tmpdir = os.path.normpath(os.path.abspath(tmpdir))
            self.assertIn(norm_tmpdir, norm_roots)
            sys.argv = orig_argv

    def test_mixed_roots_and_files(self):
        """
        Test that -r and -f options correctly process directories and file paths interchangeably.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.py")
            with open(file_path, "w") as f:
                f.write("print('hello')")
            orig_argv = sys.argv
            sys.argv = ["prog", "-r", file_path, "-f", tmpdir]
            args, extra = parse_arguments()
            norm_files = [os.path.normpath(os.path.abspath(x)) for x in args.files]
            norm_roots = [os.path.normpath(os.path.abspath(x)) for x in args.roots]
            norm_file_path = os.path.normpath(os.path.abspath(file_path))
            norm_tmpdir = os.path.normpath(os.path.abspath(tmpdir))
            self.assertIn(norm_file_path, norm_files)
            self.assertIn(norm_tmpdir, norm_roots)
            sys.argv = orig_argv

    def test_skip_patterns_parsing(self):
        """
        Test that --skip arguments are parsed correctly.
        """
        orig_argv = sys.argv
        sys.argv = ["prog", "--skip", "tests", "/tests/", "tests/filename.py"]
        args, extra = parse_arguments()
        self.assertEqual(args.skip, ["tests", "/tests/", "tests/filename.py"])
        sys.argv = orig_argv

    def test_should_skip_function(self):
        """
        Test the should_skip helper function with various skip patterns.
        """
        # Construct a sample file path that includes a 'tests' directory.
        sample_path = os.path.join(os.getcwd(), "tests", "filename.py")
        self.assertTrue(should_skip(sample_path, ["tests"]))
        self.assertTrue(should_skip(sample_path, ["/tests/"]))
        self.assertTrue(should_skip(sample_path, ["tests/filename.py"]))
        self.assertFalse(should_skip(sample_path, ["nonsense"]))

if __name__ == '__main__':
    unittest.main()

# End of savecode/tests/test_cli_args.py