"""
savecode/plugins/save.py - Plugin to save code from source files to an output file.
This module defines a plugin that reads source files and writes their contents along with a summary
to a designated output file, aggregating any errors encountered during file operations.
"""

import logging
from typing import Any, Dict, List
from io import StringIO
from pathlib import Path
from tqdm import tqdm
from savecode.plugin_manager.manager import register_plugin
from savecode.plugin_manager.decorators import handle_plugin_errors
from savecode.utils.path_utils import relative_path
from savecode.utils.error_handler import log_and_record_error
from savecode.utils.clipboard import copy as copy_clipboard

logger = logging.getLogger("savecode.plugins.save")

# Maximum file size to process (in MB)
MAX_SIZE_MB = 5


@register_plugin(order=30)
class SavePlugin:
    """Plugin that saves the content of source files to a single output file."""

    @handle_plugin_errors
    def run(self, context: Dict[str, Any]) -> None:
        """Execute the saving process using an in-memory buffer.

        Expects in context:
          - 'all_files': List of source file paths.
          - 'output': Output file path.

        Aggregates errors in context['errors'].

        Args:
            context (Dict[str, Any]): Shared context containing file lists, output path, etc.

        Returns:
            None
        """
        gathered: List[str] = context.get("all_files", [])
        output_file: str = context.get("output", "./temp.txt")

        buffer = StringIO()
        summary_details = []  # Stores paths for the summary

        try:
            for file in tqdm(gathered, desc="Processing files", unit="file"):
                rel_path = relative_path(file)

                if not Path(file).exists():
                    log_and_record_error(
                        f"{file} does not exist – skipped",
                        context,
                        logger,
                        level="warning",
                    )
                    continue

                if Path(file).stat().st_size > MAX_SIZE_MB * 1024 * 1024:
                    log_and_record_error(
                        f"Skipped {file} (>{MAX_SIZE_MB} MB)",
                        context,
                        logger,
                        level="warning",
                    )
                    continue

                try:
                    header = f"File: {rel_path}\n\n"
                    buffer.write(header)
                    with open(file, "r", encoding="utf-8", errors="replace") as f:
                        for chunk in iter(lambda: f.read(8192), ""):  # 8 KB chunks
                            buffer.write(chunk)
                    buffer.write("\n\n")
                    summary_details.append(f"- {rel_path}")
                except Exception as e:
                    error_msg = f"Error reading {file}: {e}"
                    log_and_record_error(error_msg, context, logger, exc_info=True)

            file_count = len(summary_details)
            banner = "Files saved ({}):\n{}\n\n".format(
                file_count, "\n".join(summary_details)
            )

            # Now write everything to the output file
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(banner)
                out.write(buffer.getvalue())
                footer = f"\nSaved code from {file_count} files to {output_file}\n"
                out.write(footer)

            # Prepare complete output for clipboard
            complete_output = banner + buffer.getvalue() + footer
            copy_clipboard(
                complete_output.strip()
            )  # Strip to avoid extra newlines if footer/banner have them
            logger.info("Copied concatenated code to clipboard.")

        except Exception as e:
            # Preserve legacy wording so existing tests/users can grep for it
            error_msg = (
                f"Error writing to output file {output_file}: {e} (during save process)"
            )
            log_and_record_error(error_msg, context, logger, exc_info=True)
        finally:
            buffer.close()  # Ensure StringIO buffer is closed


# End of savecode/plugins/save.py
