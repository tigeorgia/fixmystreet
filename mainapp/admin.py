from mainapp.models import EmailRule, Ward, ReportCategory,\
    City, ReportCategoryClass, FaqEntry, Councillor, Province, Report, ReportUpdate, VerifiedAuthor
from django.contrib import admin
from transmeta import canonical_fieldname

admin.site.register(EmailRule)
admin.site.register(City)
admin.site.register(Province)

class ReportCategoryClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(ReportCategoryClass,ReportCategoryClassAdmin)

class ReportCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'hint')

admin.site.register(ReportCategory, ReportCategoryAdmin)

class FaqEntryAdmin(admin.ModelAdmin):
    list_display = ('q', 'order')

admin.site.register(FaqEntry, FaqEntryAdmin)

class CouncillorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email')
    
admin.site.register(Councillor,CouncillorAdmin)


class WardAdmin(admin.ModelAdmin):
    list_display = ('id','city','number','name')
    ordering       = ['city', 'number']

admin.site.register(Ward,WardAdmin)

class VerifiedAuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')

admin.site.register(VerifiedAuthor, VerifiedAuthorAdmin)

class ReportUpdateAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'is_confirmed', 'is_fixed', 'created_at')

admin.site.register(ReportUpdate,ReportUpdateAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category','ward', 'is_fixed','is_confirmed', 'created_at')

admin.site.register(Report,ReportAdmin)


