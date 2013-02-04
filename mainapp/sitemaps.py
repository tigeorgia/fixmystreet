from django.contrib.sitemaps import Sitemap
from mainapp.models import City, Ward, ReportCategory, Report, CityWardsTotals, AllCityTotals

class MainSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Report.objects.all()
        return Ward.objects.all()
        return City.objects.all()


  
