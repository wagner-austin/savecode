"""
savecode/plugins/save.py - Plugin to save code from Python files.

This module defines a plugin that reads Python files and writes their contents
to a designated output file, aggregating any errors encountered during file operations.
"""

import os
import logging
from typing import Any, Dict, List
from savecode.plugin_manager.manager import register_plugin
from savecode.utils.path_utils import relative_path
from savecode.utils.error_handler import log_and_record_error

logger = logging.getLogger('savecode.plugins.save')

@register_plugin
class SavePlugin:
    """Plugin that saves the content of Python files to a single output file."""
    
    def run(self, context: Dict[str, Any]) -> None:
        """Execute the saving process.

        Expects in context:
          - 'all_py_files': List of Python file paths.
          - 'output': Output file path.

        Aggregates errors in context['errors'].

        Args:
            context (Dict[str, Any]): Shared context containing file lists, output path, etc.

        Returns:
            None
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
                    except Exception as e:
                        error_msg = f"Error reading {file}: {e}"
                        log_and_record_error(error_msg, context, logger, exc_info=True)
        except Exception as e:
            error_msg = f"Error writing to output file {output_file}: {e}"
            log_and_record_error(error_msg, context, logger, exc_info=True)