from . import models
from server import utils
from drf_stripe import models as m
from rest_framework import serializers
from django.utils.timezone import datetime
from django.contrib.auth import get_user_model
from drf_stripe.stripe_api.api import stripe_api

_user = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    cvc = serializers.CharField(write_only=True)
    brand = serializers.CharField(read_only=True)
    number = serializers.CharField(write_only=True)
    exp_year = serializers.CharField(write_only=True)
    exp_month = serializers.CharField(write_only=True)

    class Meta:
        model = models.Payment
        read_only_fields = "last4", "payment_id"
        fields = (
            "number",
            "exp_month",
            "exp_year",
            "cvc",
            "last4",
            "payment_id",
            "brand",
        )

    def create(self, data):
        user = self.get_user()
        try:
            payment = stripe_api.PaymentMethod.create(type="card", card=data)
            stripe_api.PaymentMethod.attach(payment.id, customer=user.customer_id)
            stripe_api.Customer.modify(
                user.customer_id,
                invoice_settings={"default_payment_method": payment.id},
            )
            return models.Payment.objects.create(
                last4=payment.card.last4,
                payment_id=payment.id,
                stripe_user=user,
                brand=payment.card.brand,
            )
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})

    def update(self, instance, data):
        user = self.get_user()
        try:
            payment = stripe_api.PaymentMethod.modify(instance.payment_id, card=data)
            setattr(instance, "last4", payment.card.last4)
            setattr(instance, "brand", payment.card.brand)
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})

    def get_user(self):
        user = self.context["request"].user
        return utils.get_or_create_stripe_user(user)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Product
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    price_id = serializers.CharField(write_only=True)

    class Meta:
        model = m.Subscription
        read_only_fields = "subscription_id", "status", "price"
        fields = "price_id", "subscription_id", "status", "price"

    def create(self, data):
        price = data.pop("price_id")
        id = self.get_user().customer_id
        try:
            subscription = stripe_api.Subscription.create(
                customer=id, items=[{"price": price}]
            )
            self.save_attributes(data, subscription, True)
            return m.Subscription.objects.create(**data)
        except Exception as e:
            print(e, "cause of create subscription error")
            raise serializers.ValidationError({"detail": str(e)})

    def update(self, instance, data):
        price = data.pop("price_id")
        try:
            subscription = stripe_api.Subscription.modify(
                instance.subscription_id, items=[{"price": price}]
            )
            self.save_attributes(instance, subscription)
            return super().update(instance, data)
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})

    def save_attributes(self, obj, data, set_user=False):
        # short = (
        #     lambda obj, attr: datetime.fromtimestamp(getattr(obj, attr))
        #     if getattr(obj, attr)
        #     else None
        # )
        # obj.update(
        #     {
        #         "ended_at": short(data, "ended_at"),
        #         "cencel_at": short(data, "cencel_at"),
        #         "trial_end": short(data, "trial_end"),
        #         "status": getattr(data, "status", None),
        #         "trial_start": short(data, "trial_start"),
        #         "subscription_id": getattr(data, "id", None),
        #         "period_end": short(data, "current_period_end"),
        #         "period_start": short(data, "current_period_start"),
        #     }
        # )
        if set_user:
            obj.update({"stripe_user": self.get_user()})
        obj.update(
            {
                "status": data.status,
                "subscription_id": data.id,
                "cancel_at_period_end": data.cancel_at_period_end,
                "ended_at": datetime.fromtimestamp(data.ended_at)
                if data.ended_at
                else None,
                "cancel_at": datetime.fromtimestamp(data.cancel_at)
                if data.cancel_at
                else None,
                "trial_end": datetime.fromtimestamp(data.trial_end)
                if data.trial_end
                else None,
                "trial_start": datetime.fromtimestamp(data.trial_start)
                if data.trial_start
                else None,
                "period_end": datetime.fromtimestamp(data.current_period_end)
                if data.current_period_end
                else None,
                "period_start": datetime.fromtimestamp(data.current_period_start)
                if data.current_period_start
                else None,
            }
        )

    def get_price(self, model):
        try:
            sub = stripe_api.Subscription.retrieve(model.subscription_id)
            subscription_object = sub["items"]["data"][0]["price"]
            return subscription_object["id"]  # returns the price id
            return subscription_object["product"]  # returns the product id
        except Exception as e:
            return None

    def get_user(self):
        user = self.context["request"].user
        return utils.get_or_create_stripe_user(user)
