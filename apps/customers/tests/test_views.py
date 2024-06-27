from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Customer


class CustomerViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.customer = Customer.objects.create(
            user=self.user, phone_number="1234567890"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_get_all_customers(self):
        url = reverse("customer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer(self):
        url = reverse("customer-detail", args=[self.customer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.customer.id)

    def test_create_customer(self):
        url = reverse("customer-list")
        new_user = User.objects.create_user(username="newuser", password="newpassword")
        data = {
            "user": new_user.id,
            "phone_number": "0987654321",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)

    def test_update_customer(self):
        url = reverse("customer-detail", args=[self.customer.id])
        data = {
            "phone_number": "0987654321",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone_number, "0987654321")

    def test_delete_customer(self):
        url = reverse("customer-detail", args=[self.customer.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)
