from django import template

from carts.models import Cart

register = template.Library()

@register.simple_tag()
def get_carts_for_user(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)