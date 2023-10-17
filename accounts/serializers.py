from rest_framework import serializers
from .models import Role
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q
import re


class CustomUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


class UserRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserLoginSerializer(AuthTokenSerializer):
    username_or_email = None  # Custom field to accept username or email

    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")

        user = None
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email)
            )
        except UserModel.DoesNotExist:
            pass

        if user is not None and user.check_password(password):
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                attrs["access_token"] = str(refresh.access_token)
                return {"access_token": attrs["access_token"]}
            else:
                raise serializers.ValidationError({"error": "User is not active."})
        else:
            raise serializers.ValidationError({"error": "Invalid credentials."})
