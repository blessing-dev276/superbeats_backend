from server import utils
from . import models, serializers
from django.db.models import Avg, Sum
from rest_framework import viewsets, mixins, response
from custom.models import Recent, Rating, Tip, Favorite


class IngredientAPI(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = utils.select_query(models.Ingredient, "recipe")

    def get_queryset(self):
        if "recipe_pk" in self.kwargs:
            return self.queryset.filter(recipe_id=self.kwargs["recipe_pk"])
        return super().get_queryset()


class InstructionAPI(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.InstructionSerializer
    queryset = utils.select_query(models.Instruction, "recipe")

    def get_queryset(self):
        if "recipe_pk" in self.kwargs:
            return self.queryset.filter(recipe_id=self.kwargs["recipe_pk"])
        return super().get_queryset()


class NutritionAPI(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.NutritionSerializer
    queryset = utils.select_query(models.Nutrition, "recipe")

    def get_queryset(self):
        if "recipe_pk" in self.kwargs:
            return self.queryset.filter(recipe_id=self.kwargs["recipe_pk"])
        return super().get_queryset()


class RecipeAPI(viewsets.ModelViewSet):
    search_fields = ["name", "category__name", "type__type"]
    queryset = utils.select_query(models.Recipe, "category", "type", "user")

    def get_queryset(self):
        if "category_pk" in self.kwargs:
            return self.queryset.filter(category_id=self.kwargs["category_pk"])
        return super().get_queryset()

    def get_serializer_class(self):
        if "pk" in self.kwargs:
            return serializers.RecipeDetailSerializer
        return serializers.RecipeSerializer

    def get_object(self):
        obj = super().get_object()
        print(obj)
        try:
            Recent.objects.get(
                user=self.request.user,
                object_id=obj.id,
                content_type=utils.get_model(models.Recipe),
            ).save()
        except Recent.DoesNotExist:
            Recent.objects.create(
                object_id=obj.id,
                user=self.request.user,
                content_type=utils.get_model(models.Recipe),
            )
        except:
            ...
        return obj


class RecipeFavoriteAPI(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeFavoriteSerializer
    search_fields = ["name", "category__name", "type__type"]

    def get_queryset(self):
        return self.request.user.favorites.filter(
            content_type=utils.get_model(models.Recipe)
        )

    def create(self, request, *args, **kwargs):
        try:
            recipe_id = request.data.get("recipe_id")
            fav = utils.one_query(Favorite, object_id=recipe_id, user=request.user)
            fav.delete()
            return response.Response({"message": "recipe removed from favorite"}, 201)
        except Exception as e:
            return super().create(request, *args, **kwargs)
        return response.Response({"message": "something went rong"}, 400)

    def get_object(self):
        obj = super().get_object()
        try:
            utils.update_create_query(
                Recent,
                user=self.request.user,
                object_id=obj.content_object.id,
                content_type=utils.get_model(models.Recipe),
            )
        except:
            print("cannot add to fav")
            ...
        return obj


class RecipePlanAPI(viewsets.ModelViewSet):
    serializer_class = serializers.RecipePlanSerializer
    search_fields = ["name", "category__name", "type__type"]

    def get_queryset(self):
        return self.request.user.plan_meals.select_related("recipe")


class RecipeHotAPI(viewsets.ReadOnlyModelViewSet):
    search_fields = ["name", "category__name", "user__username"]
    queryset = (
        utils.all_query(models.Recipe)
        .annotate(rate=Avg("ratings__rating"))
        .filter(ratings__gt=1)
        .order_by("-rate")
    )

    def get_serializer_class(self):
        if "pk" in self.kwargs:
            return serializers.RecipeDetailSerializer
        return serializers.RecipeSerializer

    def get_object(self):
        obj = super().get_object()
        print(obj)
        try:
            Recent.objects.get(
                user=self.request.user,
                object_id=obj.id,
                content_type=utils.get_model(models.Recipe),
            ).save()
        except Recent.DoesNotExist:
            Recent.objects.create(
                object_id=obj.id,
                user=self.request.user,
                content_type=utils.get_model(models.Recipe),
            )
        except:
            ...
        return obj


class RecipePersonalizedAPI(RecipeHotAPI):
    queryset = None

    def get_queryset(self):
        return self.request.user.recipes.order_by("-updated_at", "-created_at")

    def get_object(self):
        obj = super().get_object()
        print(obj)
        try:
            Recent.objects.get(
                user=self.request.user,
                object_id=obj.id,
                content_type=utils.get_model(models.Recipe),
            ).save()
        except Recent.DoesNotExist:
            Recent.objects.create(
                object_id=obj.id,
                user=self.request.user,
                content_type=utils.get_model(models.Recipe),
            )
        except:
            ...
        return obj


class RecipePopularAPI(RecipeAPI):
    queryset = (
        utils.all_query(models.Recipe)
        .annotate(times=Sum("user__recents__times"))
        .order_by("-times")
    )


class RecipeRateAPI(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeRateSerializer

    def get_queryset(self):
        return self.request.user.ratings.filter(
            content_type=utils.get_model(models.Recipe)
        )


class RecipeTipAPI(
    viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin
):
    def get_queryset(self):
        content_type = utils.get_model(models.Recipe)
        tips = utils.filter_query(
            utils.select_query(Tip, "user", "content_type"), content_type=content_type
        )
        if "recipe_pk" in self.kwargs:
            tips = tips.filter(object_id=self.kwargs["recipe_pk"])
        return tips

    def get_serializer_class(self):
        return serializers.RecipeTipSerializer


class RecipeRecentAPI(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RecipeRecentSerializer

    def get_queryset(self):
        return self.request.user.recents.filter(
            content_type=utils.get_model(models.Recipe)
        )

    def get_object(self):
        obj = super().get_object()
        try:
            utils.update_create_query(
                Recent,
                user=self.request.user,
                object_id=obj.content_object.id,
                content_type=utils.get_model(models.Recipe),
            )
        except:
            ...
        return obj


class RecipeTypeAPI(viewsets.ReadOnlyModelViewSet):
    search_fields = ["type"]
    queryset = utils.all_query(models.RecipeType)
    serializer_class = serializers.RecipeTypeSerializer


class TutorialsAPI(viewsets.ModelViewSet):
    queryset = utils.all_query(models.Tutorial)
    serializer_class = serializers.TutorialSerializer

    def get_queryset(self):
        if "category_pk" in self.kwargs:
            return self.queryset.filter(category_id=self.kwargs["category_pk"])
        return super().get_queryset()


class TutorialRateAPI(viewsets.ModelViewSet):
    search_fields = ["name", "category__name"]
    serializer_class = serializers.RecipeRateSerializer

    def get_queryset(self):
        return self.request.user.ratings.filter(
            content_type=utils.get_model(models.Tutorial)
        )
