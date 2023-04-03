from . import models
from server import utils
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["id", "name"]


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Faq
        fields = ["id", "question", "answer"]


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gallery
        fields = ["id", "file"]


class GenericSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context["request"]
        assert hasattr(request, "user"), "user is not found"

        validated_data["user"] = request.user
        validated_data["content_type"] = self.get_content_type()
        return super().create(validated_data)

    def get_content_type(self):
        assert hasattr(self, "get_model"), "must have get_model method"
        return utils.get_model(self.get_model())

    def validate_relation(self, id):
        model = self.get_model()
        if model.objects.filter(id=id).exists():
            return id
        raise serializers.ValidationError(f"{model.__name__} with id:{id} not found")


class NotificationSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField("name", read_only=True)

    class Meta:
        model = models.Notification
        fields = ["id", "seen", "type", "description", "created_at"]
