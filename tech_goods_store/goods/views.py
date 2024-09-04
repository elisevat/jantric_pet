from itertools import product
from typing import Any
from django.db.models import QuerySet
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView

from .utils import q_search
from .models import Categories, Products

# Create your views here.
class ShopView(ListView):
    model = Products
    template_name = 'goods/shop.html'
    paginate_by = 3
    context_object_name = 'goods'

    def get_queryset(self):

        category_slug = self.kwargs.get('category_slug')
        category = None
        query = self.request.GET.get('product')
        sorter = self.request.GET.get('sorter', 'pk')

        if not category_slug and not query:
            goods = super().get_queryset()
            self.title = 'Магазин'

        elif query:
            goods = q_search(query)
            # else:
            #     goods = Products.objects.all()
            self.title = f'Результаты поиска - {query}'

        else:
            category = get_object_or_404(Categories, slug=category_slug)
            self.title = category.name
            
            goods = Products.objects.filter(category=category)
    
    
                # if query:
                #     goods = q_search(query)

        if sorter and sorter != 'pk' and goods:
            goods = goods.order_by(sorter)

        self.category = category
        return goods

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context['cat_selected'] = self.category
        return context
    


def shop(request, category_slug=None):

    query = request.GET.get('product', None)
    sorter = request.GET.get('sorter', 'pk')

    if not category_slug and not query:
        category = None
        goods = Products.objects.all()
        title = 'Магазин'

    elif query:
        category = None
        goods = q_search(query)
        # else:
        #     goods = Products.objects.all()
        title = f'Результаты поиска - {query}'

    else:
        category = get_object_or_404(Categories, slug=category_slug)
        title = category.name
        goods = Products.objects.filter(category=category)
       
    
    
    # if query:
    #     goods = q_search(query)

    if sorter and sorter != 'pk' and goods:
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


# def show_product(request, product_slug):
#     product = Products.objects.get(slug=product_slug)
#     return render(request, 'goods/product.html', {'product': product, 'title': product.name})


class ShowProductView(DetailView):

    model = Products
    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    slug_field = 'slug'

    # def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
    #     product = get_object_or_404(Products, slug=self.kwargs.get(self.slug_url_kwarg))
    #     return product

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

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