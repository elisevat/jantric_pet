from django.conf.urls.static import static
from django.urls import path

from tech_goods_store import settings
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.PostsListHome.as_view(), name='list_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.PostDetailView.as_view(), name='detail_post'),
    path('category/<slug:cat_slug>/', views.CatShowList.as_view(), name='posts_cat'),
    path('<slug:post_slug>/share/', views.PostShareView.as_view(), name='post_share'),
    path('<slug:post_slug>/comment/', views.AddCommentView.as_view(), name='post_comment'),
    path('tag/<slug:tag_slug>/', views.TagShowList.as_view(), name='posts_tag'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('feed/', LatestPostsFeed(), name='posts_feed'),
    # path('search/', views.posts_search, name='posts_search'),

]

