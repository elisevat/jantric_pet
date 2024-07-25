from django.contrib.sitemaps import Sitemap
from .models import Posts


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Posts.published.all()

    def lastmod(self, obj):
        return obj.date_update