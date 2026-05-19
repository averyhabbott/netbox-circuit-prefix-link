from circuits.tables import CircuitTable
from django.test import TestCase
from netbox.registry import registry

from netbox_circuit_prefix_link.core_table_extensions import LinkedPrefixesColumn
from netbox_circuit_prefix_link.models import CircuitPrefix
from netbox_circuit_prefix_link.tests.fixtures import create_circuit, create_prefix


class LinkedPrefixesColumnRegistrationTests(TestCase):

    def test_column_is_registered_on_circuit_table(self):
        registered = registry['tables'].get(CircuitTable, {})
        self.assertIn('linked_prefixes', registered)
        self.assertIsInstance(registered['linked_prefixes'], LinkedPrefixesColumn)


class LinkedPrefixesColumnRenderTests(TestCase):

    def setUp(self):
        self.circuit = create_circuit('CID-A')
        self.column = LinkedPrefixesColumn()

    def test_renders_dash_when_no_links(self):
        self.assertIn('&mdash;', self.column.render(self.circuit.linked_prefixes))

    def test_renders_single_linked_prefix_as_anchor(self):
        prefix = create_prefix('10.0.0.0/24')
        CircuitPrefix.objects.create(circuit=self.circuit, prefix=prefix)
        html = self.column.render(self.circuit.linked_prefixes)
        self.assertIn(prefix.get_absolute_url(), html)
        self.assertIn(str(prefix), html)

    def test_renders_multiple_prefixes_comma_separated(self):
        p1 = create_prefix('10.0.0.0/24')
        p2 = create_prefix('10.0.1.0/24')
        CircuitPrefix.objects.create(circuit=self.circuit, prefix=p1)
        CircuitPrefix.objects.create(circuit=self.circuit, prefix=p2)
        html = self.column.render(self.circuit.linked_prefixes)
        self.assertIn(str(p1), html)
        self.assertIn(str(p2), html)
        self.assertIn(', ', html)
