from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

from users.models import CustomUser


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = CustomUser


class UserAdmin(BaseUserAdmin):
    list_display = (
        "login",
        "email",
        "is_active",
        "is_superuser",
        "is_staff",
        "last_login",
    )
    list_display_links = ("login",)
    fieldsets = (
        (("Персональная информация"),
         {"fields": ("login", "email", "birthday")}),
        (
            ("Статус"),
            {
                "fields": ("is_staff", "is_superuser", "is_active"),
            },
        ),
    )

    list_filter = ()
    filter_horizontal = ()
    ordering = ()
    add_fieldsets = ()
    search_fields = ()


admin.site.register(CustomUser, UserAdmin)
