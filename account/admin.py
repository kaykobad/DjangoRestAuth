from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm
from .models import User, TokenManager


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm

    # Admin Display
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'date_joined', 'is_active', 'is_staff', 'last_login')
    list_filter = ('is_active', 'is_staff', 'date_joined', 'last_login')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    ordering = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'date_joined', 'last_login')
    list_display_links = ('id', 'first_name', 'last_name')

    # Field Sets
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number'),
        }),
    )


@admin.register(TokenManager)
class TokenManagerAdmin(admin.ModelAdmin):
    # Admin Display
    list_display = ('key', 'email', 'date_created')
    list_filter = ('date_created', )
    search_fields = ('key', 'email')
    ordering = ('key', 'email', 'date_created')
    list_display_links = ('key', 'email')
