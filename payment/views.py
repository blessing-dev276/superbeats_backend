from . import serializers, models
from rest_framework import viewsets, response
from drf_stripe.stripe_api.api import stripe_api


class PaymentViewSet(viewsets.ModelViewSet):
    lookup_field = 'payment_id'
    serializer_class = serializers.PaymentSerializer

    def list(self, request):
        try:
            return super().list(request)
        except Exception as e:
            return response.Response({'detail': str(e)}, 500)

    def get_queryset(self):
        try:
            return self.request.user.stripe_user.payments.all()
        except Exception as e:
            print(e)
            return []

    def perform_destroy(self, instance):
        try:
            stripe_api.PaymentMethod.detach(instacne.payment_id)
        except Exception as e:
            print(e, 'detach payment error')
        instance.delete()


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SubscribeSerializer

    def get_queryset(self):
        return self.request.user.stripe_user.subscriptions.all()

    def perform_destroy(self, instance):
        try:
            print('try unsubscribe')
            stripe_api.Subscription.delete(instance.subscription_id)
        except Exception as e:
            print(e, 'subscription delete error')
        instance.delete()
