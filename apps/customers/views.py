from typing import Any
from rest_framework import viewsets
from .serializers import CustomerSerializer
from .selectors import get_all_customers


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    lookup_field = "id"

    def get_queryset(self) -> Any:
        return get_all_customers()
