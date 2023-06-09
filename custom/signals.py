from . import models
from datetime import datetime
from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from drf_stripe.stripe_api.api import stripe_api
from drf_stripe.models import Subscription, Product


@receiver(signals.post_save, sender=get_user_model())
def notify_user_login(sender, instance, created, *args, **kwargs):
    if (
        not created
        and kwargs.get("update_fields")
        and "last_login" in kwargs.get("update_fields")
    ):
        type, _ = models.NotificationType.objects.update_or_create(name="user login")
        models.Notification.objects.create(
            type=type,
            user=instance,
            description=f"you have logged in on {instance.last_login.strftime('%c')}",
        )


@receiver([signals.post_save, signals.post_delete], sender=models.Favorite)
def notify_favorite_change(sender, instance, created=False, *args, **kwargs):
    print(created)
    type, _ = models.NotificationType.objects.update_or_create(
        name=f"{'added' if created else 'deleted'} favorite"
    )
    models.Notification.objects.create(
        type=type,
        user=instance.user,
        description=(
            f"you have added {instance.content_object} to your favorites"
            if created
            else f"you have removed {instance.content_object} from your favorites"
        ),
    )


@receiver(signals.post_save, sender=models.Rating)
def notify_rating_change(sender, instance, created, *args, **kwargs):
    type, _ = models.NotificationType.objects.update_or_create(
        name=f"{'added' if created else 'update'} rating"
    )
    models.Notification.objects.create(
        type=type,
        user=instance.user,
        description=(
            f"you have rated {instance.content_object} {instance.rating}"
            if created
            else f"you have changed {instance.content_object} rating to {instance.rating}"
        ),
    )


@receiver(signals.post_delete, sender=models.Rating)
def notify_rating_delete(sender, instance, *args, **kwargs):
    type, _ = models.NotificationType.objects.update_or_create(name="deleted rating")
    models.Notification.objects.create(
        type=type,
        user=instance.user,
        description=f"you have deleted {instance.content_object} from your ratings",
    )


@receiver(signals.post_save, sender=Subscription)
def notify_subscription(sender, instance, created, *args, **kwargs):
    type, _ = models.NotificationType.objects.update_or_create(name="plan subscription")
    try:
        sub = stripe_api.Subscription.retrieve(model.subscription_id)
        subscription_object = sub["items"]["data"][0]["price"]
        plan_name = Product.objects.get(product_id=subscription_object["product"]).name
    except:
        plan_name = "a plan"
    models.Notification.objects.create(
        type=type,
        user=instance.stripe_user.user,
        description=f"you have subscribed to {plan_name}",
    )


@receiver(signals.post_delete, sender=Subscription)
def notify_cancel_subscription(sender, instance, *args, **kwargs):
    type, _ = models.NotificationType.objects.update_or_create(
        name="cancel subscription"
    )
    models.Notification.objects.create(
        type=type,
        user=instance.stripe_user.user,
        description="you have canceled your subscription",
    )
