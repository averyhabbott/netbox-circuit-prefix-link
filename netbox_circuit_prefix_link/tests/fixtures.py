"""Shared object factories for the test suite."""
from circuits.models import Circuit, CircuitType, Provider
from ipam.models import Prefix


def create_provider(slug='acme'):
    return Provider.objects.create(name=f'Provider {slug}', slug=slug)


def create_circuit_type(slug='transit'):
    return CircuitType.objects.create(name=f'Type {slug}', slug=slug)


def create_circuit(cid, provider=None, circuit_type=None):
    return Circuit.objects.create(
        cid=cid,
        provider=provider or create_provider(slug=f'provider-{cid.lower()}'),
        type=circuit_type or create_circuit_type(slug=f'type-{cid.lower()}'),
    )


def create_prefix(prefix='10.0.0.0/24'):
    return Prefix.objects.create(prefix=prefix)
