"""
savecode/__init__.py - Initialize the savecode package with centralized version and logging configuration.
"""

from .utils.logger import configure_logging
configure_logging()

__version__ = "1.3.0"

# Optionally expose plugin manager functions
from .plugin_manager import run_plugins, list_plugins