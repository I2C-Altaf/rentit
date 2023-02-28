from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *
# Register your models here.

class CUserAdmin(UserAdmin):
    model = Users
    list_filter = []
    list_display = ("email","username")
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "email",
                    "password",
                    "phone",
                    "username",
                    "profile",
                )
            },
        ),
        (
            "Permission Info",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1','password2','phone','username'), }),)

admin.site.register(Users, CUserAdmin)

