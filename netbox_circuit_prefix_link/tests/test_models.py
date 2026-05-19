from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase

from netbox_circuit_prefix_link.models import CircuitPrefix
from netbox_circuit_prefix_link.tests.fixtures import create_circuit, create_prefix


class CircuitPrefixModelTests(TestCase):

    def setUp(self):
        self.circuit_a = create_circuit('CID-A')
        self.circuit_b = create_circuit('CID-B')
        self.prefix_1 = create_prefix('10.0.0.0/24')
        self.prefix_2 = create_prefix('10.0.1.0/24')

    def test_create_and_reverse_accessor(self):
        link = CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        self.assertIn(link, self.circuit_a.linked_prefixes.all())
        self.assertEqual(self.prefix_1.circuit_link, link)

    def test_one_circuit_per_prefix_integrity(self):
        CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                CircuitPrefix.objects.create(circuit=self.circuit_b, prefix=self.prefix_1)

    def test_clean_rejects_duplicate_prefix_with_friendly_message(self):
        CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        link = CircuitPrefix(circuit=self.circuit_b, prefix=self.prefix_1)
        with self.assertRaises(ValidationError) as cm:
            link.clean()
        self.assertIn('prefix', cm.exception.message_dict)
        self.assertIn(str(self.circuit_a), cm.exception.message_dict['prefix'][0])

    def test_clean_allows_updating_existing_link(self):
        link = CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        link.circuit = self.circuit_b
        link.clean()  # should not raise

    def test_circuit_delete_is_protected(self):
        CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        with self.assertRaises(ProtectedError):
            self.circuit_a.delete()

    def test_prefix_delete_cascades_link(self):
        link = CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        self.prefix_1.delete()
        self.assertFalse(CircuitPrefix.objects.filter(pk=link.pk).exists())

    def test_str(self):
        link = CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        self.assertIn('->', str(link))
