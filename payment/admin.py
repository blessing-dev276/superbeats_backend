from . import models
from django.contrib import admin


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_filter = ["stripe_user"]
    search_fields = "payment_id", "stripe_user"
    list_display = "stripe_user", "payment_id", "last4"
