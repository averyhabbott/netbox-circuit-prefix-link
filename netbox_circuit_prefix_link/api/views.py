from netbox.api.viewsets import NetBoxModelViewSet

from ..filtersets import CircuitPrefixFilterSet
from ..models import CircuitPrefix
from .serializers import CircuitPrefixSerializer


class CircuitPrefixViewSet(NetBoxModelViewSet):
    queryset = (
        CircuitPrefix.objects
        .select_related('circuit', 'prefix')
        .prefetch_related('tags')
    )
    serializer_class = CircuitPrefixSerializer
    filterset_class = CircuitPrefixFilterSet
