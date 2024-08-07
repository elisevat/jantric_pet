from django.shortcuts import redirect, render

from goods.models import Products
from .models import Cart

# Create your views here.

def cart_add(request, product_slug):
    
    product = Products.objects.get(slug=product_slug)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(product=product, user=request.user)
        
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product)
    
    return redirect(request.META['HTTP_REFERER'])

def cart_change(request, product_slug):
    ...

def cart_remove(request, product_slug):
    ...