from django.urls import path
from .views import PostList, PostDetail, NewsCreate, ArticlesCreate, NewsEdit, ArticlesEdit, NewsDelete, ArticlesDelete, subscriptions
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('posts/', cache_page(20)(PostList.as_view(template_name = 'newsportal/posts.html')), name='posts'),
    path('posts/<int:pk>', PostDetail.as_view(), name='post'),
    path('posts/search', PostList.as_view(template_name = 'newsportal/posts_search.html'), name='post_search'),
    path('news/create', NewsCreate.as_view(template_name = 'newsportal/news_create.html'), name='news_create'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name = 'news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create', ArticlesCreate.as_view(template_name = 'newsportal/article_create.html'), name='article_create'),
    path('articles/<int:pk>/edit/', ArticlesEdit.as_view(), name = 'article_edit'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='article_delete'),
    path('posts/subscriptions/', subscriptions, name='subscriptions',),
]