from netbox.api.routers import NetBoxRouter

from .views import CircuitPrefixViewSet


app_name = 'netbox_circuit_prefix_link'

router = NetBoxRouter()
router.register('circuit-prefixes', CircuitPrefixViewSet)

urlpatterns = router.urls
