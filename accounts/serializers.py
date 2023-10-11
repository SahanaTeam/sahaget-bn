from rest_framework import serializers
from .models import CustomUser, Role


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "is_hero",
            "is_profile_updated",
            "country",
            "city",
            "address_line1",
            "address_line2",
            "role",
            "password",
        )

        extra_kwargs = {"password": {"write_only": True}}


class UserRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
