from django.urls import path
from . import views
from .views import (
    NewsListCreateView,
    NewsDetailView,
    NewsCommentCreateView,
    create_news_page,
    news_detail_page,
    news_list_page,
)

urlpatterns = [
    # API endpoints
    path('api/', NewsListCreateView.as_view(), name='api_news_list'),
    path('api/<int:pk>/', NewsDetailView.as_view(), name='api_news_detail'),
    path('api/<int:pk>/comment/', NewsCommentCreateView.as_view(), name='api_news_comment'),
    
    # HTML pages for viewing news
    path('news/', news_list_page, name='news_list'),
    path('news/<int:pk>/', news_detail_page, name='news_detail_page'),  # For viewing individual news detail page
    path('create/', create_news_page, name='create_news_page'),  # For creating news
    
    # News API actions
    path('news/<int:pk>/comment/', NewsCommentCreateView.as_view(), name='news_comment_api'),  # For commenting on news
]
