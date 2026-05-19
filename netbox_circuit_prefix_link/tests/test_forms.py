from django.test import TestCase

from netbox_circuit_prefix_link.forms import CircuitPrefixForm
from netbox_circuit_prefix_link.models import CircuitPrefix
from netbox_circuit_prefix_link.tests.fixtures import create_circuit, create_prefix


class CircuitPrefixFormTests(TestCase):

    def setUp(self):
        self.circuit_a = create_circuit('CID-A')
        self.circuit_b = create_circuit('CID-B')
        self.prefix_1 = create_prefix('10.0.0.0/24')
        self.prefix_2 = create_prefix('10.0.1.0/24')

    def test_valid_for_unlinked_prefix(self):
        form = CircuitPrefixForm(data={
            'circuit': self.circuit_a.pk,
            'prefix': self.prefix_1.pk,
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_rejects_already_linked_prefix(self):
        CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        form = CircuitPrefixForm(data={
            'circuit': self.circuit_b.pk,
            'prefix': self.prefix_1.pk,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('prefix', form.errors)
        self.assertIn(str(self.circuit_a), form.errors['prefix'][0])

    def test_allows_editing_existing_link(self):
        link = CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        form = CircuitPrefixForm(
            data={'circuit': self.circuit_b.pk, 'prefix': self.prefix_1.pk},
            instance=link,
        )
        self.assertTrue(form.is_valid(), form.errors)
