from django.contrib.auth import authenticate
from rest_framework import serializers

from authentication.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
            is_active=False,
        )

        # send email verification here

        return user


data = {
    "username": "abcd",
    "password": "abcd1234",
    "email": "abcd@gmail.com",
}
