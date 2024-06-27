from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "date_created")
    search_fields = ("user__username", "user__email", "phone_number")
    list_filter = ("date_created",)


admin.site.register(Customer, CustomerAdmin)
