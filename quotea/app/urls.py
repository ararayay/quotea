from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("create_quote", views.create_quote, name="create_quote"),
    path("popular_quotes", views.popular_quotes, name="popular_quotes"),
    path('<int:quote_id>/<str:reaction_type>/', views.reaction, name='reaction'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]