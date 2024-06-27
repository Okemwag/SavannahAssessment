from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .tasks import send_order_sms


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        send_order_sms.delay(sender=sender.pk, instance=instance.pk, **kwargs)
