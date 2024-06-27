from django.test import TestCase
from django.contrib.auth.models import User
from ...customers.models import Customer
from decimal import Decimal
from ..models import Order


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.customer = Customer.objects.create(
            user=self.user, phone_number="1234567890"
        )

    def test_order_creation(self):
        order = Order.objects.create(customer=self.customer, total=Decimal("100.00"))
        saved_order = Order.objects.get(id=order.id)
        self.assertEqual(saved_order.customer, self.customer)
        self.assertEqual(saved_order.total, Decimal("100.00"))
        self.assertTrue(saved_order.order_id.startswith("OD"))
        self.assertEqual(str(saved_order), saved_order.order_id)

        order2 = Order.objects.create(customer=self.customer, total=Decimal("250.50"))
        saved_order2 = Order.objects.get(id=order2.id)
        self.assertEqual(saved_order2.customer, self.customer)
        self.assertEqual(saved_order2.total, Decimal("250.50"))
        self.assertTrue(saved_order2.order_id.startswith("OD"))
        self.assertEqual(str(saved_order2), saved_order2.order_id)

        order3 = Order.objects.create(customer=self.customer, total=Decimal("0.00"))
        saved_order3 = Order.objects.get(id=order3.id)
        self.assertEqual(saved_order3.total, Decimal("0.00"))

        order4 = Order.objects.create(customer=self.customer, total=Decimal("-50.00"))
        saved_order4 = Order.objects.get(id=order4.id)
        self.assertEqual(saved_order4.total, Decimal("-50.00"))

    def test_order_auto_timestamps(self):
        order = Order.objects.create(customer=self.customer, total=Decimal("100.00"))
        self.assertIsNotNone(order.created_at)
        self.assertIsNotNone(order.updated_at)
        self.assertTrue(order.created_at <= order.updated_at)

        initial_updated_at = order.updated_at
        order.total = Decimal("150.00")
        order.save()
        self.assertNotEqual(order.updated_at, initial_updated_at)

    def test_order_id_uniqueness(self):
        order1 = Order.objects.create(customer=self.customer, total=Decimal("100.00"))
        order2 = Order.objects.create(customer=self.customer, total=Decimal("150.00"))
        self.assertNotEqual(order1.order_id, order2.order_id)

    def test_order_id_format(self):
        order = Order.objects.create(customer=self.customer, total=Decimal("100.00"))
        self.assertTrue(order.order_id.startswith("OD"))
        self.assertTrue(len(order.order_id) >= 10)
