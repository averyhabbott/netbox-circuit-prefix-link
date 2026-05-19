from ipam.models import Prefix
from netbox.plugins import PluginTemplateExtension

from .models import CircuitPrefix
from .tables import CircuitPrefixTable


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
            .select_related('circuit')
            .filter(prefix=prefix)
            .first()
        )
        return self.render(
            'netbox_circuit_prefix_link/inc/prefix_panel.html',
            extra_context={'link': link, 'prefix': prefix},
        )


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
