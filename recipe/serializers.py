from . import models
from server import utils
from rest_framework import serializers
from django.db.models import Count, Avg
from account.serializers import UserSerializer
from custom.serializers import GenericSerializer
from custom.models import Recent, Rating, Tip, Favorite


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Ingredient
        extra_kwargs = {"recipe": {"read_only": True}}


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Instruction
        extra_kwargs = {"recipe": {"read_only": True}}


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Nutrition
        extra_kwargs = {"recipe": {"read_only": True}}


class RecipeSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    reviewed = serializers.SerializerMethodField()
    ingredients = IngredientSerializer(many=True, default=None, write_only=True)
    instructions = InstructionSerializer(many=True, default=None, write_only=True)

    class Meta:
        exclude = ["user"]
        model = models.Recipe

    def create(self, validated_data):
        model = self.Meta.model
        validated_data["user"] = self.context["request"].user

        ingredients = validated_data.pop("ingredients", None)
        instructions = validated_data.pop("instructions", None)

        recipe = model.objects.create(**validated_data)
        if ingredients:
            ingredients = IngredientSerializer(None, ingredients, many=True)
            ingredients.is_valid(raise_exception=True)
            ingredients.save(recipe=recipe)

        if instructions:
            instructions = IngredientSerializer(None, instructions, many=True)
            instructions.is_valid(raise_exception=True)
            instructions.save(recipe=recipe)
        return recipe

    def get_reviewed(self, model):
        user = self.context["request"].user
        return model.ratings.filter(user=user).exists()

    def get_rating(self, model):
        try:
            attr = {"count": Count("*"), "average": Avg("rating", default=0)}
            return model.ratings.all().aggregate(**attr)
        except Exception as e:
            return None


class RecipeDetailSerializer(RecipeSerializer):
    nutritions = NutritionSerializer(many=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    instructions = InstructionSerializer(many=True, read_only=True)

    class Meta(RecipeSerializer.Meta):
        read_only_fields = ["ingredients", "nutritions", "instructions"]


class RecipeFavoriteSerializer(GenericSerializer):
    recipe_id = serializers.SlugField(source="object_id")
    recipe = RecipeSerializer(source="content_object", read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "recipe_id", "recipe"]

    def get_model(self):
        return models.Recipe

    def validate_recipe_id(self, id):
        return self.validate_relation(id)


class RecipePlanSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Meal
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "date" in validated_data:
            raise serializers.ValidationError(
                {"date": ["update operation on date not permited"]}
            )
        return super().update(instance, validated_data)


class RecipeRateSerializer(GenericSerializer):
    recipe_id = serializers.SlugField(source="object_id")
    rating = serializers.IntegerField(min_value=0, max_value=5)
    recipe = RecipeSerializer(source="content_object", read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "recipe_id", "recipe", "rating"]

    def create(self, validated_data):
        rating = validated_data.pop("rating")
        validated_data["user"] = self.context["request"].user
        validated_data["content_type"] = self.get_content_type()
        try:
            rate = Rating.objects.get(**validated_data)
            rate.rating = rating
            rate.save()
            return rate
        except Rating.DoesNotExist:
            return Rating.objects.create(**validated_data, rating=rating)
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})

    def get_model(self):
        return models.Recipe

    def validate_recipe_id(self, id):
        return self.validate_relation(id)


class RecipeRecentSerializer(GenericSerializer):
    recipe = RecipeSerializer(source="content_object", read_only=True)

    class Meta:
        model = Recent
        fields = ["id", "recipe"]

    def get_model(self):
        return models.Recipe


class RecipeTipSerializer(GenericSerializer):
    user = serializers.SerializerMethodField()
    recipe_image = serializers.SerializerMethodField()
    recipe_id = serializers.IntegerField(write_only=True, source="object_id")
    recipe = serializers.SlugRelatedField(
        "name", source="content_object", read_only=True
    )

    class Meta:
        model = Tip
        fields = [
            "id",
            "user",
            "image",
            "recipe",
            "created_at",
            "updated_at",
            "recipe_id",
            "description",
            "recipe_image",
        ]

    def get_model(self):
        return models.Recipe

    def get_user(self, model):
        return model.user.profile.avatar

    def get_recipe_image(self, model):
        return model.content_object.image


class RecipeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.RecipeType


class TutorialSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        exclude = ["user"]
        model = models.Tutorial

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def get_rating(self, model):
        attr = {"count": Count("*"), "average": Avg("rating", default=0)}
        return model.rating.aggregate(**attr)


class TutorialFavoriteSerializer(GenericSerializer):
    tutorial_id = serializers.SlugField(source="object_id")
    tutorial = TutorialSerializer(source="content_object", read_only=True)

    def get_model(self):
        return models.Tutorial

    def validate_tutorial_id(self, id):
        return self.validate_relation(id)


class TutorialRateSerializer(GenericSerializer):
    tutorial = TutorialSerializer(source="content_object", read_only=True)
    tutorial_id = serializers.SlugField(source="object_id", write_only=True)

    class Meta:
        model = Rating
        fields = ["id", "tutorial_id", "tutorial", "rating"]

    def get_model(self):
        return models.Tutorial

    def validate_recipe_id(self, id):
        return self.validate_relation(id)
