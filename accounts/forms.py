from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "is_hero",
            "is_profile_updated",
            "country",
            "city",
            "address_line1",
            "address_line2",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
