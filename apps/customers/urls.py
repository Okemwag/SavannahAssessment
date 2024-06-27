from .views import CustomerViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r"customers", CustomerViewSet, basename="customer")

urlpatterns = router.urls
