from rest_framework import serializers
from .models import Order
from ..customers.serializers import CustomerSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["order_id", "customer", "total", "created_at", "updated_at"]
        read_only_fields = ["order_id", "created_at", "updated_at"]

    def validate(self, attrs):
        data = super().validate(attrs)
        data["customer"] = self.context["request"].user.customer
        return data


class OrderDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = ["order_id", "customer", "total", "created_at", "updated_at"]
        read_only_fields = ["order_id", "created_at", "updated_at", "customer"]
