import django_tables2 as tables

from netbox.tables import NetBoxTable

from .models import CircuitPrefix


class CircuitPrefixTable(NetBoxTable):
    prefix = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = CircuitPrefix
        fields = ('pk', 'prefix', 'actions')
        default_columns = ('prefix', 'actions')
