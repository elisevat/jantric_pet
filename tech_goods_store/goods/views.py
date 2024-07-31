from django.shortcuts import render
from .models import Categories, Products

# Create your views here.

def shop(request):

    categories = Categories.objects.all()
    goods = Products.objects.all()

    context = {
        'title': 'Магазин',
        'categories': categories,
        'goods': goods,
    }
    return render(request, 'goods/shop.html', context)

def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    return render(request, 'goods/product.html', {'product': product, 'title': product.name})
