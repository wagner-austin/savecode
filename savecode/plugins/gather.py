"""
savecode/plugins/gather.py - Plugin to gather Python files from directories and validate individual file paths.
"""

import os
import logging
from typing import Any, Dict, List, Optional
from savecode.plugin_manager.manager import register_plugin
from savecode.utils.path_utils import normalize_path

logger = logging.getLogger('savecode.plugins.gather')

@register_plugin
class GatherPlugin:
    """
    Recursively gathers all Python (.py) files from specified directories
    and validates individual file paths.
    """
    def run(self, context: Dict[str, Any]) -> None:
        """
        Execute the gathering process.
        
        Expects in context:
          - 'roots': list of directories to search.
          - 'skip': list of directory names to skip.
          - 'files': list of individual Python file paths.
          
        Populates context with:
          - 'all_py_files': deduplicated list of gathered Python file paths.
        """
        all_py_files: List[str] = []
        for root in context.get('roots', []):
            normalized_root = normalize_path(root)
            if not os.path.isdir(normalized_root):
                error_msg = f"Directory {normalized_root} does not exist. Skipping."
                logger.warning(error_msg)
                context.setdefault('errors', []).append(error_msg)
            else:
                all_py_files.extend(self.gather_py_files(normalized_root, context.get('skip', []), context))
        for file in context.get('files', []):
            normalized_file = normalize_path(file)
            if os.path.isfile(normalized_file) and normalized_file.endswith(".py"):
                all_py_files.append(normalized_file)
            else:
                warning_msg = f"{file} is not a valid Python file."
                logger.warning(warning_msg)
                context.setdefault('errors', []).append(warning_msg)
        # Deduplicate while preserving order
        deduped_files = list(dict.fromkeys(all_py_files))
        context['all_py_files'] = deduped_files
        logger.info("Gathered %d unique Python files.", len(deduped_files))

    def gather_py_files(self, root_dir: str, skip_dirs: Optional[List[str]] = None, context: Dict[str, Any] = None) -> List[str]:
        """
        Recursively gather all .py files under root_dir, skipping directories in skip_dirs.
        
        :param root_dir: Directory to search.
        :param skip_dirs: List of directory names to skip.
        :param context: Optional context for error aggregation.
        :return: List of Python file paths.
        """
        root_dir = normalize_path(root_dir)
        if not os.path.isdir(root_dir):
            error_msg = f"Directory {root_dir} does not exist. Skipping."
            logger.warning(error_msg)
            if context is not None:
                context.setdefault('errors', []).append(error_msg)
            return []
        skip_dirs = set(skip_dirs or [])
        py_files: List[str] = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip specified directories
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            for fname in filenames:
                if fname.endswith(".py"):
                    file_path = os.path.join(dirpath, fname)
                    py_files.append(file_path)
        return py_files