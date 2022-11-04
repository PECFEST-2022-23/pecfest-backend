import random
import string

from django.core.validators import EmailValidator
from rest_framework import serializers

from authentication.models import User
from authentication.utils.authutil import AuthenticationUtil


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_active=False,
        )

        AuthenticationUtil().send_verification_email(user)

        return user


class OAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
        extra_kwargs = {
            "email": {
                "validators": [
                    EmailValidator,
                ]
            },
        }

    def create(self, validated_data):
        letters = string.ascii_lowercase
        password = "".join(random.choices(letters, k=8))
        user = User.objects.create_user(
            email=validated_data["email"],
            password=password,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_active=True,
        )

        return user
