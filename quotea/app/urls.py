from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("create_quote", views.create_quote, name="create_quote"),
    path("popular_quotes", views.popular_quotes, name="popular_quotes"),
    path('like/<int:quote_id>/', views.like_quote, name='like_quote'),
    path('dislike/<int:quote_id>/', views.dislike_quote, name='dislike_quote'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]