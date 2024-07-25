from django import template


register = template.Library()

@register.inclusion_tag('blog/show_paginate.html')
def show_paginate(page_obj=None, page_num=1):
    return {'page_obj': page_obj, 'page_num': page_num}
