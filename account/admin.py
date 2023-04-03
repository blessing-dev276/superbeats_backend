from . import models
from django.contrib import admin


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    list_filter = ["user"]
    search_fields = ["user"]
    date_hierarchy = "created_at"
    list_display = ["id", "user"]
    autocomplete_fields = ["user"]
    fields = ["user", "description"]


@admin.register(models.Passcode)
class PasscodeAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    date_hierarchy = "created_at"
    autocomplete_fields = ["user"]
    list_display = [
        "id",
        "user",
        "code",
        "created_at",
        "is_expired",
    ]

    def is_expired(self, model):
        return model.is_expired()

    is_expired.boolean = True
    is_expired.admin_order_field = "user"
    is_expired.short_desription = "Check if code is expired"


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    date_hierarchy = "created_at"
    fields = ["user", "phone_number", "birth_date", "avatar"]
    list_display = ["user", "birth_date", "phone_number", "updated"]

    def updated(self, model):
        return model.created_at < model.updated_at

    updated.boolean = True
    updated.admin_order_field = "user"
    updated.short_desription = "Check if user has updated his profile"


@admin.register(models.Settings)
class SettingsAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    list_filter = ["autoplay_video", "dietary_restrictions"]
    list_display = [
        "user",
        "autoplay_video",
        "measurement_system",
        "dietary_restrictions",
    ]
