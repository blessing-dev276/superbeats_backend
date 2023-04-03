from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey


class TimeModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        assert hasattr(self, "user"), "provide a user field"
        return f"{self.user.username}'s {self.__class__.__name__}"


class GenericModel(models.Model):
    object_id = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content_object = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey("contenttypes.ContentType", models.CASCADE)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]
        indexes = [models.Index(fields=["content_type", "object_id"])]

    def __str__(self):
        return f"{self.content_object} {self.__class__.__name__}"


class UniqueNameModel(TimeModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True
        ordering = ["id"]

    def __str__(self):
        return self.name.title()
