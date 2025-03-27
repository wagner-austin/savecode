"""
savecode/utils/display.py - Module for displaying file list and summary in CLI.
"""

from typing import Any, Dict, List
from savecode.utils.colors import GREEN, BLUE, CYAN, WHITE, BG_CYAN, MAGENTA, RESET
from savecode.utils.path_utils import relative_path

def display_summary(context: Dict[str, Any]) -> None:
    """
    Displays a summary of the saved Python files.
    
    Expects the context to have:
      - 'all_py_files': list of Python file paths.
      - 'output': the output file path.
    
    The function first prints the list of files (with relative paths),
    followed by a summary line indicating the total number of files saved and the output file path.
    """
    all_py_files: List[str] = context.get('all_py_files', [])
    output = context.get('output', "./temp.txt")
    
    # Print the list of saved files.
    print(f"\n{WHITE}{BG_CYAN}Files saved ({len(all_py_files)}):{RESET}")
    for file in all_py_files:
        rel_path = relative_path(file)
        print(f"{BLUE}- {rel_path}{RESET}")
    
    # Print the summary line at the bottom.
    print(f"\n{WHITE}{BG_CYAN}Saved code from {len(all_py_files)} files to {output}{RESET}\n")

# End of savecode/utils/display.py