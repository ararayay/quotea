from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Quotes, QuoteLike
from .forms import AddQuote
from .utils import get_client_ip
import random


def home(request: HttpRequest) -> HttpResponse:
    # Проверяем, есть ли в сессии ID цитаты для показа
    show_quote_id = request.session.pop('show_quote_id', None)

    if show_quote_id:
        # Показываем конкретную цитату
        try:
            quote_data = Quotes.objects.get(id=show_quote_id)
            return render(request, "random_quote.html", {"data": quote_data})
        except Quotes.DoesNotExist:
            pass

    # Обычная логика для рандомной цитаты
    all_quotes_ids = list(Quotes.objects.all().values_list('id', flat=True))
    all_quotes_weights = list(Quotes.objects.all().values_list('weight', flat=True))

    if len(all_quotes_ids) != 0:
        random_quote_id = random.choices(all_quotes_ids, all_quotes_weights, k=1)[0]
        random_quote_data = Quotes.objects.get(id=random_quote_id)

        # Обновление кол-ва просмотров
        random_quote_data.views += 1
        random_quote_data.save()

        return render(request, "random_quote.html", {"data": random_quote_data})

    return render(request, "random_quote.html", {"data": None})

@login_required
def create_quote(request: HttpRequest) -> HttpResponse:
    # Если введены данные и отправлена форма, то добавляем цитату в бд
    if request.method == 'POST':
        add_form = AddQuote(request.POST)
        if add_form.is_valid():
            new_quote = add_form.save(commit=False)

            # Проверка на дубликат (без учёта регистра)
            if Quotes.objects.filter(quote__iexact=new_quote.quote).exists():
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
    # Выбранные значения для фильтрации (по умолчанию лайки, по убыванию, 10 цитат)
    sort_by = request.GET.get('sort_by', 'likes')
    order = request.GET.get('order', 'desc')
    number = int(request.GET.get('number', '10'))

    if order == 'asc':
        sorted_quotes = Quotes.objects.order_by(sort_by)[:number]
    else:
        sorted_quotes = Quotes.objects.order_by("-" + sort_by)[:number]

    context = {
        'data': sorted_quotes,
        'sort_by': sort_by,
        'order': order,
        'number': number,
    }

    return render(request, "popular_quotes.html", context)

def reaction(request, quote_id, reaction_type):
    quote = get_object_or_404(Quotes, id=quote_id)

    # Проверка IP
    ip = get_client_ip(request)
    if QuoteLike.objects.filter(quote=quote, ip_address=ip).exists():
        quote_vote = QuoteLike.objects.get(quote=quote, ip_address=ip)

        # Если уже был поставлен лайк, убираем его при повторном нажатии и удаляем строку в бд
        if quote_vote.vote_type == reaction_type == 'like':
            quote.likes -= 1
            quote_vote.delete()
        # Если был дизлайк, и на него снова нажали, убираем его
        elif quote_vote.vote_type == reaction_type == 'dislike':
            quote.dislikes -= 1
            quote_vote.delete()
        # Если был дизлайк, а поставили лайк, то заменяем на лайк
        elif quote_vote.vote_type == 'dislike' and reaction_type == 'like':
            quote.likes += 1
            quote.dislikes -= 1

            quote_vote.vote_type = 'like'
            quote_vote.save()

            messages.info(request, 'Вы ранее поставили дизлайк этой цитате. Убрали дизлайк, поставили лайк!')
        # Если был лайк, а поставили дизлайк, заменяем на дизлайк
        else:
            quote.likes -= 1
            quote.dislikes += 1

            quote_vote.vote_type = 'dislike'
            quote_vote.save()

            messages.info(request, 'Вы ранее поставили лайк этой цитате. Убрали лайк, поставили дизлайк!')
    else:
        QuoteLike.objects.create(quote=quote, ip_address=ip, vote_type=reaction_type)
        if reaction_type == 'like':
            quote.likes += 1
        else:
            quote.dislikes += 1

    quote.save()

    # Сохраняем ID цитаты в сессии, чтобы показать именно эту цитату на главной
    request.session['show_quote_id'] = quote_id
    return redirect('home')