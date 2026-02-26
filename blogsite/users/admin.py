from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_author', 'is_approved', 'is_staff']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Permissions', {'fields': ('is_author', 'is_approved')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Permissions', {'fields': ('is_author', 'is_approved')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
