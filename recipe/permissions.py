from rest_framework.permissions import BasePermission


class RecipeCustomPermission(BasePermission):
    message = "you plan does not have the privilage to access this product"

    def has_object_permission(self, request, view, obj):
        user = getattr(request.user, "stripe_user", None)

        if (user and not obj.plan) or not obj.plan:
            return True
        elif not user and obj.plan:
            return False
        return True
