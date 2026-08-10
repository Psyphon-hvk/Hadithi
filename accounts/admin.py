from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class HadithiUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "facility_name", "county", "is_staff")
    list_filter = ("role", "county", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("HADITHI Profile", {
            "fields": ("role", "facility_name", "county", "phone_number", "bio", "avatar", "is_profile_public"),
        }),
    )
