from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application, AccessToken
from django.utils import timezone
from ...customers.models import Customer
from ..models import Order
from decimal import Decimal
import json

User = get_user_model()


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.customer = Customer.objects.create(
            user=self.user, phone_number="1234567890"
        )

        self.application = Application.objects.create(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )

        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope="read write",
            expires=timezone.now() + timezone.timedelta(days=1),
            token="secret-access-token",
            application=self.application,
        )

        self.auth_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.access_token.token}",
        }

        self.order = Order.objects.create(
            customer=self.customer, total=Decimal("100.00")
        )

    def test_list_orders(self):
        url = reverse("order-list")
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["order_id"], self.order.order_id)

    def test_retrieve_order(self):
        url = reverse("order-detail", args=[self.order.order_id])
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_id"], self.order.order_id)

    def test_create_order(self):
        url = reverse("order-list")
        data = {
            "total": "200.00",
            "customer": self.customer.id,
        }
        response = self.client.post(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data["total"], "200.00")

    def test_update_order(self):
        url = reverse("order-detail", args=[self.order.order_id])
        data = {
            "total": "150.00",
        }
        response = self.client.put(
            url, json.dumps(data), content_type="application/json", **self.auth_headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, Decimal("150.00"))

    def test_partial_update_order(self):
        url = reverse("order-detail", args=[self.order.order_id])
        data = {
            "total": "175.00",
        }
        response = self.client.patch(
            url, json.dumps(data), content_type="application/json", **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, Decimal("175.00"))

    def test_delete_order(self):
        url = reverse("order-detail", args=[self.order.order_id])
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
