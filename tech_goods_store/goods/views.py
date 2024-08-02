from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator

from .utils import q_search
from .models import Categories, Products

# Create your views here.

def shop(request, category_slug=None):

    query = request.GET.get('product', None)
    sorter = request.GET.get('sorter', 'pk')

    if not category_slug:
        category = None
        goods = Products.objects.all()
        title = 'Магазин'

    elif query:
        category = None
        if q_search(query):
            goods = q_search(query)
        else:
            goods = Products.objects.all()
        title = f'Результаты поиска - {query}'

    else:
        category = get_object_or_404(Categories, slug=category_slug)
        title = category.name
        goods = Products.objects.filter(category=category)
       
    
    
    # if query:
    #     goods = q_search(query)

    if sorter and sorter != 'pk':
        goods = goods.order_by(sorter)

    paginator = Paginator(goods, per_page=3)
    num_page = request.GET.get('page', 1)
    current_page = paginator.get_page(num_page)

    context = {
        'title': title,
        'goods': current_page,
        'cat_selected': category
    }
    return render(request, 'goods/shop.html', context)


def show_product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    return render(request, 'goods/product.html', {'product': product, 'title': product.name})


# def show_category(request, category_slug):
#     category = get_object_or_404(Categories, slug=category_slug)
#     goods = get_list_or_404(Products.objects.filter(category=category))

#     paginator = Paginator(goods, per_page=1)
#     num_page = request.GET.get('page', 1)
#     current_page = paginator.get_page(num_page)

#     context = {
#         'title': category.name,
#         'goods': current_page,
#         'cat_selected': category
#     }

#     return render(request, 'goods/shop.html', context)