import markdown
from django import template
from django.utils.safestring import mark_safe
from taggit.models import Tag

from blog.models import Category, Posts


register = template.Library()



@register.inclusion_tag('blog/show_sidebar.html')
def show_sidebar(cat_selected=0, tags_selected=0, count=4):
    cats = Category.not_empty.all()
    tags = Tag.objects.all()
    recent_posts = Posts.published.all()[:count]
    return {'cats': cats, 'cat_selected': cat_selected,
            'tags_selected': tags_selected, 'tags': tags,
            'recent_posts': recent_posts}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))