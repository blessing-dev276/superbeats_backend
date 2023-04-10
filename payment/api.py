from . import views
from rest_framework import routers
from server.routers import CustomRouter

api = routers.SimpleRouter()
api.register('products', views.ProductViewSet, 'product-products')
api.register('user/subscribe', views.SubscriptionViewSet, 'user-subscription')
api.register('user/payment-method', views.PaymentViewSet, 'user-payment-method')

urlpatterns = api.urls
