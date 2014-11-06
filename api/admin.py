from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import ApiUser


class ApiUserInline(admin.StackedInline):
    model = ApiUser
    can_delete = False


class ApiUserAdmin(UserAdmin):
    inlines = (ApiUserInline,)


admin.site.unregister(User)
admin.site.register(User, ApiUserAdmin)
