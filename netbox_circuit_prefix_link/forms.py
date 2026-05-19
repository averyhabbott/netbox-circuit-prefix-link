from django.core.exceptions import ValidationError

from circuits.models import Circuit
from ipam.models import Prefix
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField

from .models import CircuitPrefix


class CircuitPrefixForm(NetBoxModelForm):
    circuit = DynamicModelChoiceField(queryset=Circuit.objects.all())
    prefix = DynamicModelChoiceField(queryset=Prefix.objects.all())

    class Meta:
        model = CircuitPrefix
        fields = ('circuit', 'prefix', 'tags')

    def clean_prefix(self):
        prefix = self.cleaned_data['prefix']
        qs = CircuitPrefix.objects.filter(prefix=prefix)
        if self.instance.pk is not None:
            qs = qs.exclude(pk=self.instance.pk)
        existing = qs.first()
        if existing is not None:
            raise ValidationError(
                f'Prefix "{prefix}" is already linked to circuit "{existing.circuit}".'
            )
        return prefix
