from random import randint
from server import utils
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, password_validation


User = get_user_model()


class Note(models.Model):
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name="notes")

    def __str__(self):
        return f"{self.user.username}'s note"


class Passcode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True, editable=False)
    code = models.CharField(max_length=10, blank=True, editable=False)
    user = models.OneToOneField(get_user_model(), models.CASCADE, null=True, blank=True)

    def is_expired(self):
        aware = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        return aware > self.expired_at

    def validated(self):
        self.user.is_active = True
        self.user.save()
        self.delete()

    def update_user_password(self, password):
        password_validation.validate_password(password)
        self.user.set_password(password)
        self.user.save()
        self.delete()

    def save(self, **kwargs):
        self.code = randint(1000, 9999)
        self.expired_at = timezone.make_aware(
            datetime.now(), timezone.get_default_timezone()
        ) + timedelta(minutes=settings.OTP_EXPIRE_MINUTE_TIME)
        return super().save(**kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.code}"


class Profile(models.Model):
    avatar = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(get_user_model(), models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Settings(models.Model):
    sound = models.BooleanField(default=True)
    vibrate = models.BooleanField(default=True)
    feedback = models.BooleanField(default=True)
    special_offers = models.BooleanField(default=True)
    recipee_discovery = models.BooleanField(default=True)
    dietary_restrictions = models.BooleanField(default=False)
    promotion_and_discount = models.BooleanField(default=True)
    autoplay_video = models.BooleanField(null=True, blank=True)
    user = models.OneToOneField(get_user_model(), models.CASCADE)
    measurement_system = models.CharField(blank=True, max_length=255)

    class Meta:
        verbose_name_plural = "settings"

    def __str__(self):
        return f"{self.user.username}'s settings"
