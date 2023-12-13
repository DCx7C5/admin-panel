from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

AHSUser = get_user_model()


class AHSUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = AHSUser
    list_display = [
        "id",
        "email",
        "username",
        "is_staff",
        "is_active",
        "is_superuser",
        "date_joined",
        "date_modified",
        "last_login",
        "uid",
        "image",
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('image',)}),
    )
    show_full_result_count = True

admin.site.register(AHSUser, AHSUserAdmin)
