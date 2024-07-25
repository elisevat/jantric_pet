from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('product/', views.product, name='product')
]