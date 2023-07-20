from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "login",
        "email",
        "image_tmb",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "login",
        "email",
        "is_staff",
        "is_active",
    )
    list_editable = (
        "is_staff",
        "is_active",
    )
    list_display_links = (
        "login",
        "email",
        "image_tmb"
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "login",
                    "email",
                    "password",
                    "avatar",
                )
            },
        ),
        (
            "права",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                )
            },
        ),
        (
            "важные даты",
            {
                "fields": (
                    "birthday",
                    "last_login",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "login",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "birthday",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
