"""
savecode/cli.py - Entry point for savecode system. Aggregates plugins to gather and save Python code.
"""

import argparse
import os
from savecode import __version__
# Import the plugins package to ensure all plugins are registered.
import savecode.plugins
from savecode.manager.manager import run_plugins
from savecode.utils.output_manager import configure_output_path
from savecode.utils.colors import GREEN, BLUE, CYAN, RESET  # Import centralized ANSI color codes

def main():
    """
    Main entry point for the savecode CLI.
    Parses command-line arguments, builds a shared context, and runs the plugins.
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
    context = {
        'roots': args.roots,
        'files': args.files,
        'skip': args.skip,
        'output': configure_output_path(args.output),
        'extra_args': extra_args
    }
    
    run_plugins(context)
    
    # After plugins run, display a summary.
    all_py_files = context.get('all_py_files', [])
    print(f"\n{CYAN}Saved code from {len(all_py_files)} files to {context['output']}{RESET}")
    print(f"\n{GREEN}Files saved:{RESET}")
    for f in all_py_files:
        # Convert each absolute file path to a relative path from the current working directory.
        rel_path = os.path.relpath(f, os.getcwd())
        print(f"{BLUE}- {rel_path}{RESET}")
    print("\n")
    
if __name__ == "__main__":
    main()