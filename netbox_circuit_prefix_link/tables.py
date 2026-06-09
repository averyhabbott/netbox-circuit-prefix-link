import django_tables2 as tables

from netbox.tables import NetBoxTable, columns

from .models import CircuitPrefix


class CircuitPrefixTable(NetBoxTable):
    prefix = tables.Column(linkify=True)
    description = tables.Column(accessor='prefix__description', verbose_name='Description')
    utilization = columns.UtilizationColumn(
        accessor='prefix__get_utilization', orderable=False, verbose_name='Utilization'
    )
    status = columns.TemplateColumn(
        accessor='prefix__status',
        verbose_name='Status',
        template_code='{% if record.prefix %}'
                      '<span class="badge text-bg-{{ record.prefix.get_status_color }}">'
                      '{{ record.prefix.get_status_display }}</span>{% endif %}',
    )
    vlan = tables.Column(accessor='prefix__vlan', linkify=True, verbose_name='VLAN')
    vrf = tables.Column(accessor='prefix__vrf', linkify=True, verbose_name='VRF')
    tenant = tables.Column(accessor='prefix__tenant', linkify=True, verbose_name='Tenant')
    role = tables.Column(accessor='prefix__role', linkify=True, verbose_name='Role')

    class Meta(NetBoxTable.Meta):
        model = CircuitPrefix
        fields = (
            'pk', 'prefix', 'description', 'utilization', 'status',
            'vlan', 'vrf', 'tenant', 'role', 'actions',
        )
        default_columns = ('prefix', 'description', 'utilization', 'actions')
