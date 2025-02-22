"""
savecode/utils/output_manager.py - Handles configuration of the output file path.
"""

from .path_utils import normalize_path
from typing import Any

def configure_output_path(output_arg: str) -> str:
    """
    Configures the output file path.

    Always converts the provided output path to a normalized absolute path relative
    to the current working directory. This ensures that all output paths are handled
    consistently, whether they are provided as relative or absolute paths.

    :param output_arg: The output file path argument.
    :return: The normalized absolute output file path.
    """
    return normalize_path(output_arg)