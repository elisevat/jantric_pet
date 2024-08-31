from django.shortcuts import render
from django.views.generic import TemplateView

from blog.models import Posts
from goods.models import Products

# Create your views here.

# def about(request):
#     return render(request, 'main/about.html')


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Jantric - Главное'
        context['best_products'] = Products.objects.all().order_by('price')[:4]
        context['products'] = Products.objects.all()[:15]
        context['posts'] = Posts.objects.all().select_related('author')[:5]
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = 'Jantric - О нас'
        return context
    

# def index(request):
#     best_products = Products.objects.all().order_by('price')[:4]
#     products = Products.objects.all()[:15]
#     posts = Posts.objects.all().select_related('author')[:5]

#     context = {
#         'title': 'Jantric - Главное',
#         'best_products': best_products,
#         'products': products,
#         'posts': posts,
#     }

#     return render(request, 'main/index.html', context=context)