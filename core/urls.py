from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),

    # Threads
    path('threads/', views.thread_list, name='threads'),
    path('thread/<int:pk>/', views.thread_detail_view, name='thread_detail'),
    path('create-thread/', views.create_thread_view, name='create_thread'),
    

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/login/', views.login_view, name='login'),
    path('notifications/', views.notifications_view, name='notifications'),


    # Profile
    path('profile/<str:username>/', views.profile_view, name='profile'),

    # Static pages
    path('about/', views.about, name='about'),



    # Ajax
    path('thread/<int:pk>/add-comment/', views.ajax_add_comment, name='ajax_add_comment'),

]

