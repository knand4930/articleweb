from django.contrib.sitemaps import Sitemap
from news.models import News


class MyNewsSiteMap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return News.objects.all()

    def location(self, obj):
        return "/news/" + str(obj)
