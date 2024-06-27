from typing import List
from .models import Order
from ..customers.models import Customer


def get_all_orders() -> List[Order]:
    return Order.objects.all()


def get_order_by_id(order_id: str) -> Order | None:
    try:
        return Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return None


def get_orders_by_customer(customer: Customer) -> List[Order]:
    return Order.objects.filter(customer=customer)
