"""
savecode/plugins/save.py - Plugin to save code from Python files into a single output file.
"""

import os
import logging
from typing import Any, Dict, List
from savecode.plugin_manager.manager import register_plugin
from savecode.utils.path_utils import relative_path

logger = logging.getLogger('savecode.plugins.save')

@register_plugin
class SavePlugin:
    """
    Reads Python files and writes their content to a designated output file.
    Aggregates errors encountered during file operations.
    """
    def run(self, context: Dict[str, Any]) -> None:
        """
        Execute the saving process.
        
        Expects in context:
          - 'all_py_files': list of Python file paths.
          - 'output': output file path.
          
        Aggregates errors in context['errors'].
        """
        all_py_files: List[str] = context.get('all_py_files', [])
        output_file: str = context.get('output', "./temp.txt")
        try:
            with open(output_file, 'w', encoding='utf-8') as out:
                summary = "Files saved:\n"
                for file in all_py_files:
                    rel_path = relative_path(file)
                    summary += f"- {rel_path}\n"
                summary += "\n\n"
                out.write(summary)
                for file in all_py_files:
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            header = f"\nFile: {relative_path(file)}\n\n"
                            out.write(header)
                            out.write(f.read())
                            out.write("\n\n")
                    except (OSError, UnicodeDecodeError) as e:
                        error_msg = f"Error reading {file}: {e}"
                        logger.error(error_msg)
                        context.setdefault('errors', []).append(error_msg)
        except OSError as e:
            error_msg = f"Error writing to output file {output_file}: {e}"
            logger.error(error_msg)
            context.setdefault('errors', []).append(error_msg)