from django.shortcuts import render


def home(request):
    return render(request, "random_quote.html")

def create_quote(request):
    return render(request, "create_quote.html")

def popular_quotes(request):
    return render(request, "popular_quotes.html")