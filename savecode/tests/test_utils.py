"""
tests/test_utils.py - Unit tests for file path utilities and output manager functions.
"""

import os
import unittest
from savecode.utils.output_manager import configure_output_path
from savecode.utils.path_utils import relative_path, normalize_path

class TestPathUtilities(unittest.TestCase):
    def test_configure_output_path(self):
        # Test that a relative path is converted to an absolute path.
        relative = "./temp.txt"
        abs_path = configure_output_path(relative)
        self.assertTrue(os.path.isabs(abs_path))
        # Verify that normalizing the given relative path yields the same result
        self.assertEqual(abs_path, normalize_path(relative))
    
    def test_relative_path(self):
        # Create an absolute path and then get its relative version.
        current_dir = os.getcwd()
        abs_path = os.path.join(current_dir, "some", "file.py")
        rel_path = relative_path(abs_path)
        # The relative path should be a subpath of the current directory
        self.assertTrue(rel_path.startswith("some" + os.sep))
    
    def test_normalize_path(self):
        # Test that normalize_path returns a normalized absolute path.
        messy_path = "././temp/../temp.txt"
        normalized = normalize_path(messy_path)
        self.assertTrue(os.path.isabs(normalized))
        # Check that redundant parts are removed.
        self.assertNotIn("./", normalized)
    
if __name__ == '__main__':
    unittest.main()
