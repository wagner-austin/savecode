"""
savecode/plugin_manager/manager.py - Manager for savecode plugins with enhanced execution order.
This module registers plugin classes with an optional order, delays their instantiation until runtime,
and executes them in a defined order.
"""

from typing import Any, Dict, List, Tuple, Type, Callable
import logging

logger = logging.getLogger(__name__)

# Global registry for plugin classes with order
# Each entry is a tuple: (order, plugin_class)
PLUGIN_REGISTRY: List[Tuple[int, Type]] = []

def register_plugin(*args, order: int = 100) -> Callable:
    """
    Decorator to register a plugin class with an optional execution order.
    The plugin must implement a public `run(context)` method.
    
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
    # If used without arguments, the decorated class is passed directly.
    if args and len(args) == 1 and callable(args[0]):
        cls = args[0]
        PLUGIN_REGISTRY.append((order, cls))
        return cls

    def decorator(cls: Type) -> Type:
        PLUGIN_REGISTRY.append((order, cls))
        return cls

    return decorator

def run_plugins(context: Dict[str, Any]) -> None:
    """
    Instantiate and run all registered plugins in sequence using the given context.
    Plugins are executed in order of their specified 'order' value.
    Each plugin is executed in isolation; errors in one plugin are logged without halting the pipeline.
    
    :param context: Dictionary containing the context and shared data.
    """
    # Sort the registry by order value
    sorted_plugins = sorted(PLUGIN_REGISTRY, key=lambda item: item[0])
    for _, plugin_class in sorted_plugins:
        plugin_instance = plugin_class()  # Delayed instantiation
        try:
            plugin_instance.run(context)
        except Exception as e:
            logger.error("Error running plugin %s: %s", plugin_class.__name__, e, exc_info=True)

def list_plugins() -> List[str]:
    """
    List the names of all registered plugin classes in the order of execution.
    
    :return: List of plugin class names.
    """
    sorted_plugins = sorted(PLUGIN_REGISTRY, key=lambda item: item[0])
    return [cls.__name__ for _, cls in sorted_plugins]