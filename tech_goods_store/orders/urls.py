from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('show_order/<int:pk>/', views.show_order, name='show_order'),
    path('create/', views.create_order, name='create_order'),
]