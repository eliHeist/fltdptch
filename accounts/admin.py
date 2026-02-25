from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()
# Register your models here.
admin.site.site_header = 'FD Admin'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "get_groups"]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    
    def get_groups(self, obj):
        return ", ".join(obj.groups.values_list('name', flat=True)) or "No roles"
    get_groups.short_description = 'Roles'