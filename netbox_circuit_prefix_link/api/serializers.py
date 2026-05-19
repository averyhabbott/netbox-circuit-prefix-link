from circuits.api.serializers import CircuitSerializer
from ipam.api.serializers import PrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer

from ..models import CircuitPrefix


class CircuitPrefixSerializer(NetBoxModelSerializer):
    circuit = CircuitSerializer(nested=True)
    prefix = PrefixSerializer(nested=True)

    class Meta:
        model = CircuitPrefix
        fields = (
            'id', 'url', 'display', 'circuit', 'prefix', 'tags',
            'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display')
