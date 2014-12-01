from django.contrib.sitemaps import Sitemap

from apps.mainapp.models import City, Ward, Report


class MainSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Report.objects.all()
        return Ward.objects.all()
        return City.objects.all()


  
