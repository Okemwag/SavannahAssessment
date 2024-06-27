from django.db.models import QuerySet
from .models import Customer


def get_all_customers() -> QuerySet[Customer]:
    return Customer.objects.all()
