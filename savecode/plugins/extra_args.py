"""
savecode/plugins/extra_args.py - Plugin to handle extra command-line arguments.
"""

import logging
from savecode.manager.manager import register_plugin

logger = logging.getLogger(__name__)

@register_plugin
class ExtraArgsPlugin:
    """
    Plugin that processes extra command-line arguments for future features.
    Currently, it logs any extra arguments provided.
    """
    def run(self, context):
        extra_args = context.get('extra_args', [])
        if extra_args:
            logger.info("Extra arguments provided: %s", extra_args)
