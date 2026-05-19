from django.urls import include, path

from utilities.urls import get_model_urls

from . import views  # noqa: F401  -- ensures @register_model_view decorators run


urlpatterns = [
    path(
        'circuit-prefix/',
        include(get_model_urls('netbox_circuit_prefix_link', 'circuitprefix', detail=False)),
    ),
    path(
        'circuit-prefix/<int:pk>/',
        include(get_model_urls('netbox_circuit_prefix_link', 'circuitprefix')),
    ),
]
