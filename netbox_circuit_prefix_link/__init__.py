import logging

from netbox.plugins import PluginConfig, get_plugin_config


__version__ = '0.1.2'

logger = logging.getLogger('netbox.plugins.netbox_circuit_prefix_link')


class CircuitPrefixLinkConfig(PluginConfig):
    name = 'netbox_circuit_prefix_link'
    verbose_name = 'Circuit-Prefix Link'
    description = 'Link Circuits to Prefixes for IPAM/Circuits cross-reference.'
    author = 'Avery Abbott'
    author_email = 'averyhabbott@yahoo.com'
    version = __version__
    base_url = 'circuit-prefix-link'
    min_version = '4.5.0'
    max_version = '4.6.999'
    default_settings = {
        'circuit_panel': ['description', 'utilization'],
        'prefix_panel': ['provider', 'type'],
    }

    def ready(self):
        super().ready()
        from . import core_table_extensions  # noqa: F401
        from .tables import CircuitPrefixTable

        # Apply the configured Circuit-panel columns as the table's default columns.
        # 'prefix' is always shown first and 'actions' always last (permission-gated).
        available = set(CircuitPrefixTable.base_columns) - {'pk', 'prefix', 'actions'}
        configured = get_plugin_config(self.name, 'circuit_panel')
        valid = [c for c in configured if c in available]
        for bad in [c for c in configured if c not in available]:
            logger.warning("Ignoring unknown circuit_panel column: %r", bad)
        CircuitPrefixTable.Meta.default_columns = ('prefix', *valid, 'actions')


config = CircuitPrefixLinkConfig
