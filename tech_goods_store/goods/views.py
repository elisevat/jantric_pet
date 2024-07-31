from django.shortcuts import get_list_or_404, get_object_or_404, render
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

def show_product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    return render(request, 'goods/product.html', {'product': product, 'title': product.name})

def show_category(request, category_slug):
    category = get_object_or_404(Categories, slug=category_slug)
    goods = get_list_or_404(Products.objects.filter(category=category))

    context = {
        'title': category.name,
        'goods': goods,
        'cat_selected': category
    }

    return render(request, 'goods/shop.html', context)