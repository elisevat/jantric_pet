from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator
from .models import Categories, Products

# Create your views here.

def shop(request):

    goods = Products.objects.all()

    paginator = Paginator(goods, per_page=3)
    num_page = request.GET.get('page', 1)
    current_page = paginator.get_page(num_page)

    context = {
        'title': 'Магазин',
        'goods': current_page,
    }
    return render(request, 'goods/shop.html', context)


def show_product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    return render(request, 'goods/product.html', {'product': product, 'title': product.name})


def show_category(request, category_slug):
    category = get_object_or_404(Categories, slug=category_slug)
    goods = get_list_or_404(Products.objects.filter(category=category))

    paginator = Paginator(goods, per_page=1)
    num_page = request.GET.get('page', 1)
    current_page = paginator.get_page(num_page)

    context = {
        'title': category.name,
        'goods': current_page,
        'cat_selected': category
    }

    return render(request, 'goods/shop.html', context)