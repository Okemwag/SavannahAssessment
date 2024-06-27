from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Customer


class CustomerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="johndoe", password="password123", email="johndoe@example.com"
        )

    def test_customer_creation(self):
        customer = Customer.objects.create(user=self.user, phone_number="0797306927")
        self.assertIsNotNone(customer.id)
        self.assertEqual(customer.user, self.user)
        self.assertEqual(customer.phone_number, "0797306927")
        self.assertIsNotNone(customer.date_created)

    def test_customer_str(self):
        customer = Customer.objects.create(user=self.user, phone_number="0797306927")
        self.assertEqual(str(customer), self.user.username)
