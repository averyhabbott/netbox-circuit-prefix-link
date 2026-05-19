from django.core.exceptions import ValidationError
from django.db import models

from netbox.models import NetBoxModel


class CircuitPrefix(NetBoxModel):
    circuit = models.ForeignKey(
        to='circuits.Circuit',
        on_delete=models.PROTECT,
        related_name='linked_prefixes',
    )
    prefix = models.OneToOneField(
        to='ipam.Prefix',
        on_delete=models.CASCADE,
        related_name='circuit_link',
    )

    class Meta:
        ordering = ('circuit', 'prefix')
        verbose_name = 'Circuit-Prefix Link'
        verbose_name_plural = 'Circuit-Prefix Links'

    def __str__(self):
        return f'{self.circuit} -> {self.prefix}'

    def clean(self):
        super().clean()
        if self.prefix_id is not None:
            existing = (
                CircuitPrefix.objects
                .filter(prefix=self.prefix)
                .exclude(pk=self.pk)
                .first()
            )
            if existing is not None:
                raise ValidationError({
                    'prefix': f'This prefix is already linked to circuit {existing.circuit}.',
                })

    def get_absolute_url(self):
        # No standalone detail page exists for CircuitPrefix (panels-only UX),
        # so NetBoxModel's default reverse to a 'circuitprefix' view would 500.
        # Redirect to the prefix's detail page, which is where the link's
        # Edit/Unlink panel lives.
        return self.prefix.get_absolute_url()
