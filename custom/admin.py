from . import models
from django.contrib import admin


@admin.register(models.Category, models.NotificationType)
class NameUniqueAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    date_hierarchy = "created_at"
    list_display = ["id", "name"]


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_filter = ["user", "content_type"]
    list_display = ["favorite_item", "user", "created_at", "updated"]

    def favorite_item(self, model):
        return model.content_object

    def updated(self, model):
        return model.created_at < model.updated_at

    updated.boolean = True
    updated.admin_order_field = "user"
    updated.short_desription = "user updated his favorite product"


@admin.register(models.Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_filter = ["user"]
    search_fields = ["user"]
    list_display = ["id", "user", "file", "created_at", "updated"]

    def updated(self, model):
        return model.created_at < model.updated_at

    updated.boolean = True
    updated.admin_order_field = "user"
    updated.short_desription = "user updated his gellery collection"


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_filter = ["user", "type", "seen"]
    list_display = ["id", "type", "user", "seen"]


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    list_filter = ["user", "content_type"]
    list_display = ["product_item", "user", "rating", "created_at", "updated"]

    def product_item(self, model):
        return model.content_object

    def updated(self, model):
        return model.created_at < model.updated_at

    updated.boolean = True
    updated.admin_order_field = "user"
    updated.short_desription = "user updated his rating"


@admin.register(models.Recent)
class RecentAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    list_filter = ["user", "content_type"]
    list_display = ["item", "user", "times", "created_at", "updated"]

    def item(self, model):
        return model.content_object

    def updated(self, model):
        return model.created_at < model.updated_at

    updated.boolean = True
    updated.admin_order_field = "user"
    updated.short_desription = "user revisit the item"


@admin.register(models.Tip)
class TipAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    list_filter = ["user", "content_type"]
    list_display = ["product", "user", "created_at", "updated"]

    def product(self, model):
        return model.content_object

    def updated(self, model):
        return model.created_at < model.updated_at

    updated.boolean = True
    updated.admin_order_field = "user"
    updated.short_desription = "user updated his tips"
