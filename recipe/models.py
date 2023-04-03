from django.db import models
from server import utils, models as m
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation

User = get_user_model()


class Ingredient(m.TimeModel):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=255, blank=True)
    recipe = models.ForeignKey("Recipe", models.CASCADE, related_name="ingredients")

    def __str__(self):
        return f"{self.recipe.name}'s ingredient".lower()


class Instruction(m.TimeModel):
    image = models.URLField(blank=True)
    description = models.CharField(max_length=255, blank=True)
    recipe = models.ForeignKey("Recipe", models.CASCADE, related_name="instructions")

    def __str__(self):
        return f"{self.recipe.name}'s instruction".lower()


class Meal(m.TimeModel):
    date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, models.PROTECT, related_name="plan_meals")
    recipe = models.ForeignKey("Recipe", models.CASCADE, related_name="plan_meals")


class Nutrition(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    recipe = models.ForeignKey("Recipe", models.CASCADE, related_name="nutritions")

    def __str__(self):
        return f"{self.recipe.name}'s nutrition".lower()


class Recipe(m.TimeModel):
    description = models.TextField()
    tips = GenericRelation("custom.tip")
    tips = GenericRelation("custom.tip")
    name = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    ratings = GenericRelation("custom.rating")
    recents = GenericRelation("custom.recent")
    image = models.URLField(blank=True, null=True)
    favorites = GenericRelation("custom.favorite")
    category = models.ForeignKey("custom.category", models.PROTECT)
    user = models.ForeignKey(User, models.PROTECT, related_name="recipes")
    type = models.ForeignKey("RecipeType", models.PROTECT, blank=True, null=True)
    plan = models.OneToOneField(
        "drf_stripe.product", models.SET_NULL, null=True, blank=True
    )


class RecipeType(m.TimeModel):
    type = models.CharField(unique=True, max_length=255)

    class Meta:
        ordering = ["type"]

    def __str__(self):
        return self.type.title()


class Tutorial(m.TimeModel):
    name = models.CharField(max_length=255)
    video = models.URLField(blank=True, null=True)
    category = models.ForeignKey("custom.category", models.PROTECT)
    user = models.ForeignKey(User, models.PROTECT, related_name="tutorials")
