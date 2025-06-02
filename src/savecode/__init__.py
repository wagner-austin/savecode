"""
savecode/__init__.py
Keep runtime version in sync with packaging metadata.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0.dev"

__all__ = ["run_plugins", "list_plugins"]
from .plugin_manager import run_plugins, list_plugins
