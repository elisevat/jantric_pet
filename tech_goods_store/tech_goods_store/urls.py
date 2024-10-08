"""
URL configuration for tech_goods_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.db import router
from django.urls import path, include, re_path
from blog.sitemaps import PostSitemap
from tech_goods_store import settings
from debug_toolbar.toolbar import debug_toolbar_urls

from blog import views

from rest_framework import routers

from goods.views import ProductsViewSet

sitemaps = {
    'posts': PostSitemap,
}

router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('shop/', include('goods.urls', namespace='goods')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('user/', include('users.urls', namespace='users')),
    path('cart/', include('carts.urls', namespace='carts')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/posts/', views.PostsAPIList.as_view()),
    path('api/v1/postslist/<int:pk>/', views.PostsAPIUpdate.as_view()),
    path('api/v1/postslist/<int:pk>/', views.PostsAPIDestroy.as_view()),

    path(r'api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path(r'api/v1/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
    
admin.site.site_header = 'Администрирование Jantric'
admin.site.index_title = 'Данные сайта'