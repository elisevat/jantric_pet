from django.template.loader import render_to_string
from .utils import get_user_carts
from .models import Cart


class CartMixin:

    def get_cart(self, request, product=None, pk=None):
        if request.user.is_authenticated:
            query_kwargs = {'user': request.user}
        
        else:
            query_kwargs = {'session_key': request.session.session_key}

        if product:
            query_kwargs['product'] = product

        if pk:
            query_kwargs['pk'] = pk

        return Cart.objects.filter(**query_kwargs).first()
    
    def render_included_cart(self, request):
        user_cart = get_user_carts(request)
        return render_to_string(
        'carts/includes/included_cart_with_buttom.html', {'carts': user_cart}, request=request)
    
    def render_included_main_cart(self, request):
        user_cart = get_user_carts(request)
        return render_to_string(
        'carts/includes/cart_main_include.html', {'carts': user_cart}, request=request)
    