from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()
# Register your models here.
admin.site.site_header = 'Dot Scholar Admin'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "school", "is_school_owner"]