from . import models
from server import utils
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = ["id", "description"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class PasscodeSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)

    class Meta:
        model = models.Passcode
        fields = ["id", "email", "user"]
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        user = utils.get_object_or_404(models.User, email=validated_data["email"])
        code, _ = utils.update_create_query(models.Passcode, user=user)
        return code

    def update(self, instance, validated_data):
        instance.save()
        return instance

    def validate_email(self, email):
        utils.get_object_or_404(models.User, email=email)
        return email

    def validate_code(self, code):
        obj = utils.get_object_or_404(models.Passcode, code=code)
        if obj.is_expired():
            raise serializers.ValidationError("code has expired")
        return code


class PasscodeVerifySerializer(PasscodeSerializer):
    class Meta(PasscodeSerializer.Meta):
        fields = ["id", "code", "email"]


class PasswordResetSerializer(PasscodeSerializer):
    code = serializers.CharField()
    password = serializers.CharField()

    class Meta(PasscodeSerializer.Meta):
        fields = ["code", "password"]

    def create(self, validated_data):
        code = utils.get_object_or_404(models.Passcode, code=validated_data["code"])
        code.update_user_password(validated_data["password"])
        return validated_data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        exclude = ["id", "user"]

    def update(self, instance, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().update(instance, validated_data)


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["user"]
        model = models.Settings

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(default={})
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = models.User
        extra_kwargs = {"email": {"required": True}, "password": {"write_only": True}}
        fields = [
            "id",
            "full_name",
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "profile",
        ]

    def create(self, validated_data):
        profile = validated_data.pop("profile", None)
        user = models.User.objects.create_user(**validated_data)
        setattr(self.context["request"], "user", user)
        profile = ProfileSerializer(
            user.profile, profile, partial=True, context=self.context
        )
        profile.is_valid(raise_exception=True)
        profile.save()
        return user

    def validate_email(self, email):
        if models.User.objects.filter(email=email).exists():
            raise serializers.ValidationError("email already exists")
        return email

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password
