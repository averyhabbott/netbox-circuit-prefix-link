from netbox.plugins import PluginConfig


class CircuitPrefixLinkConfig(PluginConfig):
    name = 'netbox_circuit_prefix_link'
    verbose_name = 'Circuit-Prefix Link'
    description = 'Link Circuits to Prefixes for IPAM/Circuits cross-reference.'
    version = '0.1.0'
    base_url = 'circuit-prefix-link'
    min_version = '4.5.0'
    max_version = '4.6.999'


config = CircuitPrefixLinkConfig
