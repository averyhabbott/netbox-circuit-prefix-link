from netbox.plugins import PluginConfig


__version__ = '0.1.1'


class CircuitPrefixLinkConfig(PluginConfig):
    name = 'netbox_circuit_prefix_link'
    verbose_name = 'Circuit-Prefix Link'
    description = 'Link Circuits to Prefixes for IPAM/Circuits cross-reference.'
    version = __version__
    base_url = 'circuit-prefix-link'
    min_version = '4.5.0'
    max_version = '4.6.999'

    def ready(self):
        super().ready()
        from . import core_table_extensions  # noqa: F401


config = CircuitPrefixLinkConfig
