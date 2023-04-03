from . import models
from custom import models as m
from django.contrib import admin


class TipInline(admin.TabularInline):
    extra = 0
    model = m.Tip
    fields = ["quantity", "name", "description"]


class IngredientInline(admin.TabularInline):
    extra = 0
    model = models.Ingredient
    fields = ["quantity", "name", "description"]


class InstructionInline(admin.StackedInline):
    extra = 0
    model = models.Instruction
    fields = ["image", "description"]


class NutritionInline(admin.StackedInline):
    extra = 0
    model = models.Nutrition
    fields = ["name", "recipe", "description"]


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    date_hierarchy = "created_at"
    list_filter = ["category", "user", "type"]
    inlines = [IngredientInline, InstructionInline, NutritionInline]
    list_display = [
        "id",
        "name",
        "user",
        "time",
        "type",
        "category",
        "nutritions",
        "ingredients",
        "instructions",
    ]
    fieldsets = [
        [None, {"fields": ["name", "time", "image", "description"]}],
        ["Additional Info", {"fields": ["user", "category", "type","plan"]}],
    ]

    def nutritions(self, model):
        return model.nutritions.count()

    def ingredients(self, model):
        return model.ingredients.count()

    def instructions(self, model):
        return model.instructions.count()


@admin.register(models.RecipeType)
class RecipeTypeAdmin(admin.ModelAdmin):
    search_fields = ["type"]
    list_display = ["id", "type", "recipes", "created_at", "updated_at"]

    def recipes(self, model):
        return model.recipe_set.count()

    recipes.integer = True
    recipes.admin_order_field = "type"
    recipes.short_desription = "Number of recipes under current type"


@admin.register(models.Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["category", "user"]
    autocomplete_fields = ["category"]
    list_display = ["id", "name", "created_at", "updated_at"]


@admin.register(models.Meal)
class MealAdmin(admin.ModelAdmin):
    list_filter = ["user", "recipe"]
    search_fields = ["user", "recipe"]
    list_display = ["id", "recipe", "user", "date", "created_at", "updated_at"]
