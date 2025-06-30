from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Quotes
import random


def home(request: HttpRequest) -> HttpResponse:
    # Создание списка id и весов для выбора рандомной строки из базы данных
    all_quotes = list(Quotes.objects.all())
    all_quotes_ids = []
    all_quotes_weights = []

    for object in all_quotes:
        all_quotes_ids.append(object.id)
        all_quotes_weights.append(object.weight)

    random_quote_id = random.choices(all_quotes_ids, all_quotes_weights, k=1)[0]
    random_quote_data = Quotes.objects.get(id=random_quote_id)

    # Обновление кол-ва просмотров
    random_quote_data.views += 1
    random_quote_data.save()

    return render(request, "random_quote.html", {"data": random_quote_data})

def create_quote(request: HttpRequest) -> HttpResponse:
    return render(request, "create_quote.html")

def popular_quotes(request: HttpRequest) -> HttpResponse:
    # Сортировка по лайкам и выбор первых 10 цитат
    most_popular_quotes = Quotes.objects.order_by('-likes')[:10]
    return render(request, "popular_quotes.html", {"data": most_popular_quotes})