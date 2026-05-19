import django_filters
from circuits.models import Circuit
from ipam.models import Prefix
from netbox.filtersets import NetBoxModelFilterSet

from .models import CircuitPrefix


class CircuitPrefixFilterSet(NetBoxModelFilterSet):
    circuit_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Circuit.objects.all(),
        label='Circuit (ID)',
    )
    prefix_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.all(),
        label='Prefix (ID)',
    )

    class Meta:
        model = CircuitPrefix
        fields = ('id', 'circuit_id', 'prefix_id')
