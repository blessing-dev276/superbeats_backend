from server import utils
from . import serializers, models
from rest_framework_simplejwt import views
from rest_framework import viewsets, mixins, permissions, response


class NoteAPI(viewsets.ModelViewSet):
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        return self.request.user.notes.all()


class PasscodeResendAPI(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.PasscodeSerializer

    def get_user(self):
        email = self.request.data.get("email")
        return utils.get_object_or_404(models.User, email=email)

    def create(self, request, *args, **kwargs):
        if self.get_user().is_active:
            return response.Response({"message": "user account is already active"}, 204)
        return super().create(request, *args, **kwargs)


class PasscodeActivateAPI(PasscodeResendAPI):
    def create(self, request, *args, **kwargs):
        code = utils.get_object_or_404(models.Passcode, user=self.get_user())
        instance = self.get_serializer(code, request.data)
        instance.is_valid(raise_exception=True)
        code.validated()
        return response.Response({"message": "account activated successfully"}, 200)


class PasswordResetAPI(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.PasscodeSerializer

    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
            return response.Response(
                {"message": "verification code sent successfully"}, 200
            )
        except Exception as e:
            return response.Response({"detail": str(e)}, 400)


class PasswordChangeAPI(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        l = super().create(request, *args, **kwargs)
        print(l)
        return response.Response({"message": "password reset successfully"}, 200)


class ProfileAPI(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        try:
            return self.request.user.profile
        except Exception as e:
            return models.Profile.objects.create(user=self.request.user)


class RefreshAPI(views.TokenRefreshView):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SettingsAPI(
    viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin
):
    serializer_class = serializers.SettingsSerializer

    def get_object(self):
        try:
            return self.request.user.settings
        except Exception as e:
            return models.Settings.objects.create(user=self.request.user)


class SigninAPI(views.TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SignupAPI(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return response.Response({"message": "user created successfully"}, 201)


class UserAPI(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user
