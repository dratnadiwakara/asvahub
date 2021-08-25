from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models.auth import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'classes': ('collapse',), 'fields': ('address', 'phone_number')}),
        ('Investor info', {'classes': ('collapse',), 'fields': ('first_name', 'last_name', 'nic_number')}),
        ('Borrower Info', {'classes': ('collapse',), 'fields': ('legal_name', 'contact_name')}),
        ('Permissions', {'classes': ('collapse',), 'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser')}),
        ('Group Permissions', {'classes': ('collapse',), 'fields': ('groups', 'user_permissions')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    # filter_horizontal = ()


admin.site.register(User, UserAdmin)
