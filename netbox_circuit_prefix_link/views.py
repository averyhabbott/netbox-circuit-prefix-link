from netbox.views.generic import ObjectDeleteView, ObjectEditView
from utilities.views import register_model_view

from .forms import CircuitPrefixForm
from .models import CircuitPrefix


@register_model_view(CircuitPrefix, name='add', detail=False)
@register_model_view(CircuitPrefix, name='edit')
class CircuitPrefixEditView(ObjectEditView):
    queryset = CircuitPrefix.objects.all()
    form = CircuitPrefixForm


@register_model_view(CircuitPrefix, name='delete')
class CircuitPrefixDeleteView(ObjectDeleteView):
    queryset = CircuitPrefix.objects.all()
