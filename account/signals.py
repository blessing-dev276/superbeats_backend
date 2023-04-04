from . import models
from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from drf_stripe.stripe_api.api import stripe_api
from server.utils import email_user, get_or_create_stripe_user


@receiver(signals.post_save, sender=get_user_model())
def create_profile_and_send_otp(sender, instance, created, *args, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)
        models.Settings.objects.create(user=instance)

        if not (instance.is_staff or instance.is_superuser):
            models.Passcode.objects.create(user=instance)
            instance.is_active = False
            instance.save()

            email_user(
                instance,
                "Account activation",
                "account/activation.html",
                {"code": instance.passcode.code},
            )


@receiver(signals.post_save, sender=get_user_model())
def create_user_stripe_account(sender, instance, created, *args, **kwargs):
    if created:
        try:
            get_or_create_stripe_user(instance)
        except Exception as e:
            print(e, "failed to create user stripe data")


@receiver(signals.post_delete, sender=get_user_model())
def delete_user_stripe_account(sender, instance, *args, **kwargs):
    try:
        stripe_api.Customer.delete(instance.stripe_user.customer_id)
    except Exception as e:
        print(e, "failed to delete user stripe data")
