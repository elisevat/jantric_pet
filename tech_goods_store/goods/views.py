from django.shortcuts import render
from .models import Categories, Products

# Create your views here.

def shop(request):
    context = {
        'title': 'Магазин',
        'categories': Categories.objects.all(),
        'goods': Products.objects.all(),
    }
    return render(request, 'goods/shop.html', context)

def product(request):
    return render(request, 'goods/product.html')