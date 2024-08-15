from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from goods.models import Products
from .utils import get_user_carts
from .models import Cart

# Create your views here.

def cart_add(request):
    product_id = request.POST.get('product_id')
    product = Products.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(product=product, user=request.user)
        
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product)

    else:
        carts = Cart.objects.filter(product=product, session_key=request.session.session_key)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(product=product, session_key=request.session.session_key)


    user_cart = get_user_carts(request)

    cart_items_html = render_to_string(
        'carts/includes/included_cart_with_buttom.html', {'carts': user_cart}, request=request)
    
    response_data = {
        'message': 'Товар добавлен в корзину',
        'cart_items_html': cart_items_html
    }

    return JsonResponse(response_data)


def cart_change(request):
    for key, value in request.POST.items():
        if key.isdigit():
            cart = Cart.objects.get(pk=key)
            if int(value) > 1:
                cart.quantity = value
                cart.save()
            else:
                cart.quantity = 1
                cart.save()
    return redirect(request.META['HTTP_REFERER'])

def cart_remove(request):
    cart_id = request.POST.get('cart_id')
    is_main = request.POST.get('is_main')
    print(request.POST, cart_id, '\n', is_main)

    cart = Cart.objects.get(pk=cart_id)
    if cart:
        cart.delete()

    user_cart = get_user_carts(request)
    
    cart_main_items_html = render_to_string(
        'carts/includes/cart_main_include.html', {'carts': user_cart}, request=request)

    cart_items_html = render_to_string(
        'carts/includes/included_cart_with_buttom.html', {'carts': user_cart}, request=request)
    
    
    
    response_data = {
        'message': 'Товар удален из корзины',
        'cart_items_html': cart_items_html,
        'cart_main_items_html': cart_main_items_html
    }
    
    return JsonResponse(response_data)