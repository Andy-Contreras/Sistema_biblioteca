from django.contrib import admin
from .models import CustomUser, Libro


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_active', 'is_staff')
