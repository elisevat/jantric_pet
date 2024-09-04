from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('', views.ShopView.as_view(), name='shop'),
    path('<slug:category_slug>/', views.ShopView.as_view(), name='category'),
    path('product/<slug:product_slug>/', views.ShowProductView.as_view(), name='product')
]