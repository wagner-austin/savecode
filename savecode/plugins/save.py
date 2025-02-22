"""
savecode/plugins/save.py - Plugin to save code from Python files into a single output file with enhanced error handling.
This version aggregates errors during file reading and writing instead of exiting immediately.
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
    Plugin that reads Python files and writes their content to a designated output file.
    
    Aggregates errors encountered during reading and writing processes.
    """
    def run(self, context: Dict[str, Any]) -> None:
        """
        Execute the saving process.
        
        Expects the following keys in context:
          - 'all_py_files': list of Python file paths gathered by the GatherPlugin.
          - 'output': the output file path where the combined code should be saved.
        
        Aggregates errors in context['errors'] instead of terminating immediately.
        """
        all_py_files: List[str] = context.get('all_py_files', [])
        output_file: str = context.get('output', "./temp.txt")
        try:
            with open(output_file, 'w', encoding='utf-8') as out:
                # Write a summary header at the beginning of the file.
                summary = "Files saved:\n"
                for file in all_py_files:
                    rel_path = relative_path(file)
                    summary += f"- {rel_path}\n"
                summary += "\n\n"
                out.write(summary)
                
                # Now write the contents of each file.
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