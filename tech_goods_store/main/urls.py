from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', cache_page(60)(views.AboutView.as_view()), name='about'),
]