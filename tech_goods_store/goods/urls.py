from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('<slug:category_slug>/', views.shop, name='category'),
    path('product/<slug:product_slug>/', views.show_product, name='product')
]