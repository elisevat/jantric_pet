from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('product/<slug:product_slug>/', views.product, name='product')
]