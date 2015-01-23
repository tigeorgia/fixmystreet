from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from apps.users.models import FMSUser, FMSSettings
from apps.users.forms import FMSUserCreationForm, FMSUserChangeForm

class FMSSettingsInline(admin.TabularInline):
    model = FMSSettings


class FMSUserAdmin(UserAdmin):
    inlines = [FMSSettingsInline,]
    fieldsets = (
        (_('Credentials'), {'fields': ('username',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (_('Credentials'), {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    form = FMSUserChangeForm
    add_form = FMSUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)


admin.site.register(FMSUser, FMSUserAdmin)
