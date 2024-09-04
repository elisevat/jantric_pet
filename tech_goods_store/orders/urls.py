from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('show_order/<int:pk>/', views.ShowOrderView.as_view(), name='show_order'),
    path('create/', views.CreateOrderView.as_view(), name='create_order'),
]