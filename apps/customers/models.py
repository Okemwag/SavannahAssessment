from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer", default=None
    )
    phone_number = models.CharField(_("phone number"), max_length=15)
    date_created = models.DateTimeField(
        _("date created"), auto_now_add=True, editable=False
    )

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def __str__(self) -> str:
        return self.user.username
