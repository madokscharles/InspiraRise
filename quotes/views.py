import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Category, DailyAffirmation, BlogPost, Subscriber
from .forms import QuoteForm, SubscriptionForm

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
    if request.method == "POST":
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            return redirect('subscription_success')  # Redirects to a success page after subscribing
    else:
        subscription_form = SubscriptionForm()

    affirmations = DailyAffirmation.objects.all().order_by('-created_at')
    context = {
        'subscription_form': subscription_form,
        'affirmations': affirmations,
    }
    
    return render(request, 'quotes/daily_affirmations.html', context)


def blog(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'quotes/blog.html', {'posts': posts})


def subscription_success(request):
    return render(request, 'quotes/subscription_success.html')