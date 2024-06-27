from typing import Any, Dict
from celery import shared_task

from ..customers.models import Customer
from .models import Order
import requests
from urllib.parse import urlencode
from django.conf import settings

username = settings.AFRICASTALKING_USERNAME
api_key = settings.AFRICASTALKING_API_KEY


@shared_task
def send_order_sms(sender_pk: int, instance_pk: int, **kwargs: Dict[str, Any]) -> None:
    customer = Customer.objects.get(pk=sender_pk)
    instance = Order.objects.get(pk=instance_pk)
    message = (
        f"Hello {customer.first_name}, your order has been created successfully. "
        f"Your order ID {instance.order_id} is being worked on. "
        "Thank you for shopping with us."
    )
    data = {
        "from": "28757",
        "username": username,
        "to": customer.phone_number,
        "message": message,
    }
    headers = {
        "apiKey": api_key,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    response = requests.post(
        "https://api.sandbox.africastalking.com/version1/messaging",
        headers=headers,
        data=urlencode(data),
    )

    response.raise_for_status()
