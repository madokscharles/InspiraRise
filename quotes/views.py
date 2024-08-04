import requests
from django.shortcuts import render
from .models import Category
from .forms import QuoteForm

# Create your views here.
def get_quotes_from_api(category=None):
    api_url = "https://api.quotable.io/random"
    params = {'tags': category.name} if category else {}
    response = requests.get(api_url, params=params)
    return response.json()


def get_author_info(author):
    if author.lower() == "anonymous":
        return None

    wikipedia_api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{author.replace(' ', '_')}"
    response = requests.get(wikipedia_api_url)
    if response.status_code == 200:
        data = response.json()
        return data.get('extract')
    return None


def quote_view(request):
    form = QuoteForm(request.GET or None)
    quotes = None

    if form.is_valid():
        category = form.cleaned_data['category']
        quotes = get_quotes_from_api(category)
        author_info = get_author_info(quotes['author'])
        quotes['author_info'] = author_info if author_info else 'Author is anonymous'

    return render(request, 'quotes/quote_view.html', {'form': form, 'quotes': quotes})


def daily_affirmations(request):
    return render(request, 'quotes/daily_affirmations.html')


def blog(request):
    return render(request, 'quotes/blog.html')