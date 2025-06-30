from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("create_quote", views.create_quote, name="create_quote"),
    path("popular_quotes", views.popular_quotes, name="popular_quotes"),
]