from django.db import models
from server import utils, models as m
from django.contrib.auth import get_user_model


class Category(m.UniqueNameModel):
    class Meta:
        verbose_name_plural = "categories"


class Favorite(m.GenericModel):
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name="favorites")


class Faq(models.Model):
    answer = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return self.question.title()


class Gallery(m.TimeModel):
    file = models.URLField()
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name="galleries")

    class Meta:
        verbose_name_plural = "galleries"


class NotificationType(m.UniqueNameModel):
    ...


class Notification(m.TimeModel):
    description = models.TextField()
    seen = models.BooleanField(default=False)
    type = models.ForeignKey(NotificationType, models.PROTECT)
    user = models.ForeignKey(
        get_user_model(), models.CASCADE, related_name="notifications"
    )


class Rating(m.GenericModel):
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name="ratings")


class Recent(m.GenericModel):
    times = models.PositiveIntegerField()
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name="recents")

    def save(self, *args, **kwargs):
        self.times += 1
        return super().save(*args, **kwargs)


class Tip(m.GenericModel):
    description = models.TextField()
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name="tips")
