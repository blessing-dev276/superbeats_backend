from rest_framework import serializers
from django.contrib.auth import authenticate, models
from rest_framework_simplejwt.tokens import RefreshToken


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(required=False, write_only=None)
    username = serializers.CharField(required=False, write_only=None)

    def validate(self, attrs):
        """
        It takes the username and password from the request, and uses the Django authenticate function
        to check if the user exists in the database. If the user exists, it creates a refresh token and
        returns it. If the user doesn't exist, it raises a validation error

        :param attrs: The validated data from the serializer
        :return: The refresh token and the access token.
        """
        user = authenticate(**attrs)
        if user:
            refresh = RefreshToken.for_user(user)
            models.update_last_login(None, user)
            return {"refresh": str(refresh), "access": str(refresh.access_token)}
        else:
            raise serializers.ValidationError("Invalid credentials")
