from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('add/<slug:product_slug>/', views.cart_add, name='cart_add'),
    path('change/<slug:product_slug>/', views.cart_change, name='cart_change'),
    path('remove/<slug:product_slug>/', views.cart_remove, name='cart_remove')
]