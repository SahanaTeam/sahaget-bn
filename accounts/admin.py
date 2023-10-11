from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Role


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "user_id",
        "username",
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
    ]

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
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
            },
        ),
    )


class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
