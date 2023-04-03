from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, backends

User = get_user_model()


class CustomAuthBackend(backends.ModelBackend):
    def authenticate(self, request, *args, **kwargs):
        email = kwargs.get("email")
        username = kwargs.get("username")
        password = kwargs.get("password")

        if not (email or username) and password:
            raise ValidationError(
                {"details": "provide email or username along with password"}
            )

        try:
            user = User.objects.get(
                **({"email": email} if email else {"username": username})
            )
        except Exception as e:
            raise ValidationError(
                f"{'email' if email else 'username'} or password incorrect"
            )

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        raise ValidationError({"details": "unable to authenticate user"})

    def user_can_authenticate(self, user):
        is_active = getattr(user, "is_active")
        if is_active == None:
            raise ValidationError({"details": "user account is deleted"})
        return is_active
