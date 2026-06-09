import logging

from ipam.models import Prefix
from netbox.plugins import PluginTemplateExtension, get_plugin_config

from .models import CircuitPrefix
from .tables import CircuitPrefixTable

logger = logging.getLogger('netbox.plugins.netbox_circuit_prefix_link')

# Available Circuit attributes for the Prefix panel, mapped to (label, render kind).
# The Circuit link itself is always rendered first, independent of this mapping.
CIRCUIT_PANEL_FIELDS = {
    'provider': ('Provider', 'link'),
    'provider_account': ('Account', 'link'),
    'type': ('Type', 'link'),
    'status': ('Status', 'status'),
    'tenant': ('Tenant', 'link'),
    'install_date': ('Installed', 'value'),
    'termination_date': ('Terminates', 'value'),
    'commit_rate': ('Commit Rate (Kbps)', 'value'),
    'description': ('Description', 'value'),
}


class CircuitLinkedPrefixes(PluginTemplateExtension):
    models = ['circuits.circuit']

    def right_page(self):
        request = self.context['request']
        circuit = self.context['object']
        links = (
            circuit.linked_prefixes
            .restrict(request.user, 'view')
            .select_related('prefix')
        )
        table = CircuitPrefixTable(links)
        table.configure(request)
        return self.render(
            'netbox_circuit_prefix_link/inc/circuit_panel.html',
            extra_context={'table': table, 'circuit': circuit},
        )


class PrefixLinkedCircuit(PluginTemplateExtension):
    models = ['ipam.prefix']

    def right_page(self):
        request = self.context['request']
        prefix = self.context['object']
        link = (
            CircuitPrefix.objects
            .restrict(request.user, 'view')
            .select_related('circuit', 'circuit__provider', 'circuit__provider_account',
                            'circuit__type', 'circuit__tenant')
            .filter(prefix=prefix)
            .first()
        )
        rows = self._build_rows(link.circuit) if link else []
        return self.render(
            'netbox_circuit_prefix_link/inc/prefix_panel.html',
            extra_context={'link': link, 'prefix': prefix, 'rows': rows},
        )

    @staticmethod
    def _build_rows(circuit):
        """Build the configured Circuit-attribute rows for the Prefix panel."""
        configured = get_plugin_config('netbox_circuit_prefix_link', 'prefix_panel')
        rows = []
        for name in configured:
            if name not in CIRCUIT_PANEL_FIELDS:
                logger.warning("Ignoring unknown prefix_panel column: %r", name)
                continue
            label, kind = CIRCUIT_PANEL_FIELDS[name]
            if kind == 'status':
                rows.append({
                    'label': label,
                    'kind': 'status',
                    'value': circuit.get_status_display(),
                    'color': circuit.get_status_color(),
                })
            else:
                rows.append({'label': label, 'kind': kind, 'value': getattr(circuit, name)})
        return rows


class IPAddressLinkedCircuit(PluginTemplateExtension):
    models = ['ipam.ipaddress']

    def right_page(self):
        request = self.context['request']
        ip = self.context['object']
        # IPAddress has no get_parents() helper. Use the same query NetBox's
        # own IPAddress detail view uses to populate its "Parent prefixes"
        # table (see ipam/views.py: IPAddressView.get_extra_context).
        parent_prefixes = (
            Prefix.objects
            .restrict(request.user, 'view')
            .filter(vrf=ip.vrf, prefix__net_contains_or_equals=str(ip.address.ip))
        )
        links = (
            CircuitPrefix.objects
            .restrict(request.user, 'view')
            .select_related('circuit', 'prefix')
            .filter(prefix__in=parent_prefixes)
        )
        if not links.exists():
            return ''
        return self.render(
            'netbox_circuit_prefix_link/inc/ipaddress_panel.html',
            extra_context={'links': links, 'ip': ip},
        )


template_extensions = [
    CircuitLinkedPrefixes,
    PrefixLinkedCircuit,
    IPAddressLinkedCircuit,
]
