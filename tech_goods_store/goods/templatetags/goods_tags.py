
from django import template

from goods.models import Categories


register = template.Library()

@register.simple_tag()
def get_categories():
    return Categories.objects.all()

# @register.inclusion_tag()
# def show_categories(cat_slug=None):
#     if cat_slug:
#         cat = Categories.objects.filter(slug=cat_slug)