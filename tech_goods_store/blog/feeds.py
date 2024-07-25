from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Posts


class LatestPostsFeed(Feed):
    title = 'Список постов'
    link = reverse_lazy('blog:list_post')
    description = 'Новые посты в Jantric'

    def items(self):
        return Posts.published.all()[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(item.content, 30)

    def item_pubdate(self, item):
        return item.date_publish