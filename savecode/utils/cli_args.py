"""
savecode/utils/cli_args.py - Module for parsing CLI arguments and merging source inputs.
This module provides a function to parse CLI arguments, including an optional positional
argument 'source' that supports commands like 'savecode .' or 'savecode ./'.
"""

import argparse
import os
from savecode import __version__

def parse_arguments():
    """
    Parse command-line arguments for the savecode tool.

    Returns:
        tuple: A tuple containing:
            - argparse.Namespace: Parsed arguments.
            - list: List of extra arguments not recognized by the parser.
    """
    parser = argparse.ArgumentParser(
        description="Save the full code from Python files in specified directories and individual files to a single output file."
    )
    parser.add_argument(
        '-r', '--roots',
        nargs='*',
        default=[],
        help="One or more directories or file paths to search for Python files. Accepts both directories and individual files."
    )
    parser.add_argument(
        '-f', '--files',
        nargs='*',
        default=[],
        help="One or more directories or file paths to include. Accepts both directories and individual files."
    )
    parser.add_argument(
        '-o', '--output',
        default="./temp.txt",
        help="Output file path. Defaults to './temp.txt'."
    )
    parser.add_argument(
        '--skip',
        nargs='*',
        default=['rnn_src'],
        help="Subdirectory names or file paths to skip (default: ['rnn_src'])."
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit."
    )
    parser.add_argument(
        '--log-level',
        default='WARNING',
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to WARNING."
    )
    # New optional positional argument to support commands like "savecode ." or "savecode ./"
    parser.add_argument(
        'source',
        nargs='*',
        default=[],
        help="Optional positional argument(s) specifying directories or file paths."
    )
    args, extra_args = parser.parse_known_args()

    # Append positional source arguments into roots/files lists.
    for src in args.source:
        normalized_src = os.path.normpath(os.path.abspath(src))
        if os.path.isdir(normalized_src):
            args.roots.append(src)
        else:
            args.files.append(src)

    # Reclassify the provided roots and files based on actual type.
    def reclassify(paths):
        dirs = []
        files = []
        for p in paths:
            normalized_p = os.path.normpath(os.path.abspath(p))
            if os.path.isdir(normalized_p):
                dirs.append(p)
            else:
                files.append(p)
        return dirs, files

    roots_dirs, roots_files = reclassify(args.roots)
    files_dirs, files_files = reclassify(args.files)

    args.roots = roots_dirs + files_dirs
    args.files = roots_files + files_files

    return args, extra_args

# End of savecode/utils/cli_args.py