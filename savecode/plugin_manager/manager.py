"""
savecode/plugin_manager/manager.py - Plugin Manager for savecode.
Encapsulates plugin registration and execution within a PluginManager class.
"""

from typing import Any, Dict, List, Tuple, Type, Callable
import logging

logger = logging.getLogger(__name__)

class PluginManager:
    """
    Encapsulates the registry and execution of plugins.
    """
    def __init__(self):
        self.registry: List[Tuple[int, Type]] = []

    def register_plugin(self, plugin_class: Type, order: int = 100) -> Type:
        """
        Registers a plugin class with an optional execution order.
        
        :param plugin_class: The plugin class to register.
        :param order: The execution order; lower values run earlier.
        :return: The plugin class.
        """
        self.registry.append((order, plugin_class))
        return plugin_class

    def run_plugins(self, context: Dict[str, Any]) -> None:
        """
        Instantiates and runs all registered plugins in sequence.
        
        :param context: Dictionary containing the shared context and data.
        """
        sorted_plugins = sorted(self.registry, key=lambda item: item[0])
        for _, plugin_class in sorted_plugins:
            plugin_instance = plugin_class()  # Delayed instantiation
            try:
                plugin_instance.run(context)
            except Exception as e:
                logger.error("Error running plugin %s: %s", plugin_class.__name__, e, exc_info=True)

    def list_plugins(self) -> List[str]:
        """
        Lists the names of all registered plugin classes in the order of execution.
        
        :return: List of plugin class names.
        """
        sorted_plugins = sorted(self.registry, key=lambda item: item[0])
        return [cls.__name__ for _, cls in sorted_plugins]

# Create a global instance of PluginManager
plugin_manager = PluginManager()

def register_plugin(*args, order: int = 100) -> Callable:
    """
    Decorator to register a plugin class with an optional execution order.
    
    Can be used as:
        @register_plugin
        class MyPlugin:
            ...
    or
        @register_plugin(order=10)
        class MyPlugin:
            ...
    
    :param order: An integer specifying the execution order; lower values run earlier.
    :return: A decorator that registers the plugin class.
    """
    if args and len(args) == 1 and callable(args[0]):
        cls = args[0]
        return plugin_manager.register_plugin(cls, order=order)
    
    def decorator(cls: Type) -> Type:
        return plugin_manager.register_plugin(cls, order=order)
    
    return decorator

def run_plugins(context: Dict[str, Any]) -> None:
    """
    Runs all registered plugins using the global PluginManager instance.
    
    :param context: Dictionary containing the context and shared data.
    """
    plugin_manager.run_plugins(context)

def list_plugins() -> List[str]:
    """
    Lists the names of all registered plugin classes in order.
    
    :return: List of plugin class names.
    """
    return plugin_manager.list_plugins()