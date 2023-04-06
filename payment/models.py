from django.db import models
from drf_stripe.models import StripeUser


class Payment(models.Model):
    last4 = models.CharField(max_length=10)
    brand = models.CharField(max_length=255, blank=True)
    payment_id = models.CharField(max_length=255, unique=True)
    stripe_user = models.ForeignKey(StripeUser, models.CASCADE, related_name="payments")

    def __str__(self):
        return self.stripe_user.user.username
