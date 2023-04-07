from rest_framework.permissions import BasePermission


class RecipeCustomPermission(BasePermission):
    message = "you plan does not have the privilage to access this product"

    def has_object_permission(self, request, view, obj):
        user = request.user
        subscriptions = (
            user.stripe_user.subscriptions.first()
            if hassattr(user, "stripe_user")
            else None
        )

        if not ((subscriptions or obj.plan) or obj.plan):
            return True
        return True
