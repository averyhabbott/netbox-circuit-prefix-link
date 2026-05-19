from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.constants import TOKEN_PREFIX
from users.models import Token

from netbox_circuit_prefix_link.models import CircuitPrefix
from netbox_circuit_prefix_link.tests.fixtures import create_circuit, create_prefix


User = get_user_model()


class CircuitPrefixAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='apitester', password='x', is_superuser=True)
        self.token = Token.objects.create(user=self.user)  # defaults to v2
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {TOKEN_PREFIX}{self.token.key}.{self.token.token}'
        )

        self.circuit_a = create_circuit('CID-A')
        self.circuit_b = create_circuit('CID-B')
        self.prefix_1 = create_prefix('10.0.0.0/24')
        self.prefix_2 = create_prefix('10.0.1.0/24')

        self.list_url = reverse('plugins-api:netbox_circuit_prefix_link-api:circuitprefix-list')

    def test_unauthenticated_write_rejected(self):
        anon = APIClient()
        response = anon.post(self.list_url, {'circuit': self.circuit_a.pk, 'prefix': self.prefix_1.pk}, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create(self):
        response = self.client.post(
            self.list_url,
            {'circuit': self.circuit_a.pk, 'prefix': self.prefix_1.pk},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(CircuitPrefix.objects.count(), 1)

    def test_list_and_filter_by_circuit(self):
        CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        CircuitPrefix.objects.create(circuit=self.circuit_b, prefix=self.prefix_2)
        response = self.client.get(self.list_url, {'circuit_id': self.circuit_a.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_delete(self):
        link = CircuitPrefix.objects.create(circuit=self.circuit_a, prefix=self.prefix_1)
        detail_url = reverse('plugins-api:netbox_circuit_prefix_link-api:circuitprefix-detail', args=[link.pk])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CircuitPrefix.objects.filter(pk=link.pk).exists())
