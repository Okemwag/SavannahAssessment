from rest_framework import viewsets, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response

from .serializers import OrderSerializer, OrderDetailSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    lookup_field = "order_id"

    def get_queryset(self):

        return self.request.user.customer.orders.all()

    def get_serializer_class(self) -> type:
        if self.action in ["retrieve", "update", "partial_update"]:
            return OrderDetailSerializer
        return OrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
