from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        "email",
        "username",
        "is_staff",
    ]
    fieldsets = BaseUserAdmin.fieldsets + ((None, {"fields": ("age",)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + ((None, {"fields": ("age",)}),)
