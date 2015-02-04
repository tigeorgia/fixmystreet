from django.contrib import admin
from django.contrib.gis import admin as gisadmin

from apps.mainapp.models import EmailRule, Ward, ReportCategory, \
    City, ReportCategoryClass, FaqEntry, Councillor, Province, Report, ReportUpdate, VerifiedAuthor


admin.site.register(EmailRule)
admin.site.register(City)
admin.site.register(Province)

class LocalOpenLayersMixin(object):
    openlayers_url = 'https://www.chemikucha.ge/static/js/OpenLayers.js'

class ReportCategoryClassAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(ReportCategoryClass, ReportCategoryClassAdmin)


class ReportCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'hint')


admin.site.register(ReportCategory, ReportCategoryAdmin)


class FaqEntryAdmin(admin.ModelAdmin):
    list_display = ('q', 'order')


admin.site.register(FaqEntry, FaqEntryAdmin)


class CouncillorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email')


admin.site.register(Councillor, CouncillorAdmin)


class WardAdmin(LocalOpenLayersMixin, gisadmin.GeoModelAdmin):
    list_display = ('id', 'city', 'number', 'name')
    ordering = ['city', 'number']
    display_wkt = True

admin.site.register(Ward, WardAdmin)


class VerifiedAuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')


admin.site.register(VerifiedAuthor, VerifiedAuthorAdmin)


class ReportUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')


admin.site.register(ReportUpdate, ReportUpdateAdmin)


class ReportAdmin(LocalOpenLayersMixin, gisadmin.GeoModelAdmin):
    list_display = ('title', 'category', 'ward', 'status', 'created_at')


admin.site.register(Report, ReportAdmin)


