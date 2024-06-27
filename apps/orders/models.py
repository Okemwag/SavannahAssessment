from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.utils import timezone
from django.utils.crypto import get_random_string

from ..customers.models import Customer


def generate_order_id():
    date_str = timezone.now().strftime("%Y%m%d")
    random_str = get_random_string(length=3).upper()
    return f"OD{date_str}{random_str}"


class Order(models.Model):
    order_id = models.CharField(
        _("order ID"),
        max_length=30,
        default=generate_order_id,
        db_index=True,
        unique=True,
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name=_("customer"),
        on_delete=models.CASCADE,
        related_name="orders",
    )
    total = models.DecimalField(
        _("total"), max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.order_id
