"""
savecode/cli.py - Entry point for savecode system. Aggregates plugins to gather and save Python code.
This version aggregates errors encountered during plugin execution and reports them before exiting.
"""

import argparse
import os
import sys
from typing import Any, Dict, List
from savecode import __version__
# Import the plugins package to ensure all plugins are registered.
import savecode.plugins
from savecode.plugin_manager.manager import run_plugins
from savecode.utils.output_manager import configure_output_path
from savecode.utils.colors import GREEN, BLUE, CYAN, RESET
from savecode.utils.display import display_summary     # Import display module for summary output

def main() -> None:
    """
    Main entry point for the savecode CLI.
    Parses command-line arguments, builds a shared context, runs the plugins,
    displays a summary of the saved files, and reports any errors encountered.
    """
    parser = argparse.ArgumentParser(
        description="Save the full code from Python files in specified directories and individual files to a single output file."
    )
    parser.add_argument(
        '-r', '--roots',
        nargs='*',
        default=[],
        help="One or more root directories to search for Python files."
    )
    parser.add_argument(
        '-f', '--files',
        nargs='*',
        default=[],
        help="One or more individual Python file paths to include."
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
        help="Subdirectory names to skip (default: ['rnn_src'])."
    )
    # Add version flag.
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit."
    )
    # Allow additional unknown arguments for future expansion.
    args, extra_args = parser.parse_known_args()
    
    # Build a shared context for all plugins.
    context: Dict[str, Any] = {
        'roots': args.roots,
        'files': args.files,
        'skip': args.skip,
        'output': configure_output_path(args.output),
        'extra_args': extra_args,
        'errors': []  # Initialize error aggregation list
    }
    
    run_plugins(context)
    
    # If errors were aggregated during plugin execution, report and exit with error.
    if context['errors']:
        print("\nErrors encountered:")
        for error in context['errors']:
            print(f"- {error}")
        sys.exit(1)
    
    # Display a summary of the saved files using the centralized display function.
    display_summary(context)
    
if __name__ == "__main__":
    main()