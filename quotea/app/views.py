from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Quotes, QuoteLike
from .forms import AddQuote
from .utils import get_client_ip
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
    # Если введены данные и отправлена форма, то добавляем цитату в бд
    if request.method == 'POST':
        add_form = AddQuote(request.POST)
        if add_form.is_valid():
            new_quote = add_form.save(commit=False)

            # Проверка на дубликат
            if Quotes.objects.filter(quote=new_quote.quote).exists():
                messages.error(request, 'Такая цитата уже есть.')
            else:
                # Проверка на количество цитат одного источника
                if Quotes.objects.filter(source=new_quote.source).count() == 3:
                    messages.error(request, 'У одного источника не должно быть больше 3 цитат.')
                else:
                    new_quote.save()
                    messages.info(request, 'Цитата успешно добавлена!')
            return redirect('home')
    
    # Если запрошена страница, выводим форму
    else:
        add_form = AddQuote()
        return render(request, "create_quote.html", {"form": add_form})

def popular_quotes(request: HttpRequest) -> HttpResponse:
    # Сортировка по лайкам и выбор первых 10 цитат
    most_popular_quotes = Quotes.objects.order_by('-likes')[:10]
    return render(request, "popular_quotes.html", {"data": most_popular_quotes})

def like_quote(request, quote_id):
    # Лайк
    quote = get_object_or_404(Quotes, id=quote_id)

    # Проверка IP
    ip = get_client_ip(request)
    if QuoteLike.objects.filter(quote=quote, ip_address=ip).exists():
        quote_vote = QuoteLike.objects.get(quote=quote, ip_address=ip)

        if quote_vote.vote_type == 'like':
            messages.error(request, 'Вы уже лайкнули эту цитату.')
        else:
            quote.likes += 1
            quote.dislikes -= 1
            quote.save()

            quote_vote.vote_type = 'like'
            quote_vote.save()

            messages.info(request, 'Вы ранее дизлайкнули эту цитату. Убрали дизлайк, поставили лайк!')
    else:
        QuoteLike.objects.create(quote=quote, ip_address=ip, vote_type='like')
        quote.likes += 1
        quote.save()
    
    return render(request, "random_quote.html", {"data": quote})

def dislike_quote(request, quote_id):
    # Дизлайк
    quote = get_object_or_404(Quotes, id=quote_id)

    # Проверка IP
    ip = get_client_ip(request)
    if QuoteLike.objects.filter(quote=quote, ip_address=ip).exists():
        quote_vote = QuoteLike.objects.get(quote=quote, ip_address=ip)

        if quote_vote.vote_type == 'dislike':
            messages.error(request, 'Вы уже дизлайкнули эту цитату.')
        else:
            quote.likes -= 1
            quote.dislikes += 1
            quote.save()

            quote_vote.vote_type = 'dislike'
            quote_vote.save()

            messages.info(request, 'Вы ранее лайкнули эту цитату. Убрали лайк, поставили дизлайк!')
    else:
        QuoteLike.objects.create(quote=quote, ip_address=ip, vote_type='dislike')
        quote.dislikes += 1
        quote.save()

    return render(request, "random_quote.html", {"data": quote})