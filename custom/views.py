from server import utils
from . import serializers, models
from rest_framework import viewsets, mixins, permissions


class CategoryAPI(viewsets.ReadOnlyModelViewSet):
    search_fields = ["name"]
    queryset = utils.all_query(models.Category)
    serializer_class = serializers.CategorySerializer

class FaqAPI(viewsets.ReadOnlyModelViewSet):
    search_fields = ["name"]
    queryset = utils.all_query(models.Faq)
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.FaqSerializer


class GalleryAPI(viewsets.ModelViewSet):
    search_fields = ["name"]
    serializer_class = serializers.GallerySerializer

    def get_queryset(self):
        return self.request.user.galleries.all() or []


class NotificationAPI(viewsets.ReadOnlyModelViewSet):
    search_fields = ["name"]
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        return self.request.user.notifications.all() or []

    def get_object(self):
        model = super().get_object()
        model.seen = True
        model.save()
        return model
