from .views import OrderViewSet
from rest_framework import routers

routers = routers.SimpleRouter()
routers.register(r"orders", OrderViewSet, basename="order")

urlpatterns = routers.urls
