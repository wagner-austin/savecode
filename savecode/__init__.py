"""
savecode/__init__.py - Initializes the savecode package with version information.
"""

__version__ = "2.0.1"

# Optionally expose plugin manager functions.
from .plugin_manager import run_plugins, list_plugins