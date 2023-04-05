from . import views
from custom.api import router as parent
from rest_framework_nested import routers


router = routers.SimpleRouter()

router.register("recipees", views.RecipeAPI, "recipees")
router.register("tutorials", views.TutorialsAPI, "tutorials")
router.register("plan-recipee", views.RecipePlanAPI, "plan-recipee")
router.register("hot-recipees", views.RecipeHotAPI, "hot-recipees")
router.register("rate-recipee", views.RecipeRateAPI, "rate-recipee")
router.register("recipee-types", views.RecipeTypeAPI, "recipee-types")
router.register("rate-tutorial", views.TutorialRateAPI, "rate-tutorial")
router.register("recent-recipees", views.RecipeRecentAPI, "recent-recipees")
router.register("popular-recipees", views.RecipePopularAPI, "popular-recipees")
router.register("favorite-recipees", views.RecipeFavoriteAPI, "favorite-recipees")
router.register(
    "personalized-recipees", views.RecipePersonalizedAPI, "personalized-recipees"
)

recipee_router = routers.NestedSimpleRouter(parent, "categories", lookup="category")
recipee_router.register("recipees", views.RecipeAPI, "recipees")

nested_router = routers.NestedSimpleRouter(router, "recipees", lookup="recipee")
nested_router.register("tips", views.RecipeTipAPI, "tips")
nested_router.register("nutritions", views.NutritionAPI, "nutritions")
nested_router.register("ingredients", views.IngredientAPI, "ingredients")
nested_router.register("instructions", views.InstructionAPI, "instructions")

replies_router = routers.NestedSimpleRouter(nested_router, "tips", lookup="tip")

urlpatterns = (
    router.urls + recipee_router.urls + nested_router.urls + replies_router.urls
)
