from django.shortcuts import render

# Create your views here.

def shop(request):
    return render(request, 'goods/shop.html')

def product(request):
    return render(request, 'goods/product.html')