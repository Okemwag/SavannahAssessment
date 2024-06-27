from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer", "total", "created_at", "updated_at")
    search_fields = (
        "order_id",
        "customer__name",
    )
    list_filter = ("created_at", "updated_at", "customer")
    ordering = ("-created_at",)
    readonly_fields = ("order_id", "created_at", "updated_at")


admin.site.register(Order, OrderAdmin)
