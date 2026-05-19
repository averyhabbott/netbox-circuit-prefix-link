from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from netbox_circuit_prefix_link.models import CircuitPrefix
from netbox_circuit_prefix_link.template_content import (
    CircuitLinkedPrefixes,
    IPAddressLinkedCircuit,
    PrefixLinkedCircuit,
)
from netbox_circuit_prefix_link.tests.fixtures import create_circuit, create_prefix


User = get_user_model()


class TemplateExtensionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='paneltester', password='x', is_superuser=True)
        self.factory = RequestFactory()
        self.circuit = create_circuit('CID-A')
        self.prefix = create_prefix('10.0.0.0/24')

    def _request(self):
        request = self.factory.get('/')
        request.user = self.user
        return request

    def test_circuit_panel_lists_linked_prefix(self):
        CircuitPrefix.objects.create(circuit=self.circuit, prefix=self.prefix)
        ext = CircuitLinkedPrefixes(context={'object': self.circuit, 'request': self._request()})
        html = ext.right_page()
        self.assertIn(str(self.prefix), html)

    def test_prefix_panel_shows_circuit_when_linked(self):
        CircuitPrefix.objects.create(circuit=self.circuit, prefix=self.prefix)
        ext = PrefixLinkedCircuit(context={'object': self.prefix, 'request': self._request()})
        html = ext.right_page()
        self.assertIn(str(self.circuit), html)

    def test_prefix_panel_shows_none_when_unlinked(self):
        ext = PrefixLinkedCircuit(context={'object': self.prefix, 'request': self._request()})
        html = ext.right_page()
        self.assertIn('None', html)

    def test_ipaddress_panel_empty_when_no_parent_link(self):
        from ipam.models import IPAddress
        ip = IPAddress.objects.create(address='10.0.0.5/24')
        ip.refresh_from_db()  # coerce .address to IPNetwork
        ext = IPAddressLinkedCircuit(context={'object': ip, 'request': self._request()})
        self.assertEqual(ext.right_page(), '')

    def test_ipaddress_panel_resolves_via_parent_prefix(self):
        from ipam.models import IPAddress
        CircuitPrefix.objects.create(circuit=self.circuit, prefix=self.prefix)
        ip = IPAddress.objects.create(address='10.0.0.5/24')
        ip.refresh_from_db()
        ext = IPAddressLinkedCircuit(context={'object': ip, 'request': self._request()})
        html = ext.right_page()
        self.assertIn(str(self.circuit), html)
        self.assertIn(str(self.prefix), html)
