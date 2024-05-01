from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from social.accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from social.accounts.models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ()}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ()}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'is_online',)
