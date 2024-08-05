import requests
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Category, DailyAffirmation, BlogPost, Subscriber
from .forms import QuoteForm, SubscriptionForm, DailyAffirmationForm, BlogPostForm

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
    today = timezone.now().date()
    current_affirmation = DailyAffirmation.objects.filter(created_at__date=today).first()

    if request.method == "POST":
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            return redirect('subscription_success')  # Redirects to a success page after subscribing
    else:
        subscription_form = SubscriptionForm()

    previous_affirmations = DailyAffirmation.objects.filter(created_at__date__lt=today).order_by('-created_at')
    context = {
        'subscription_form': subscription_form,
        'current_affirmation': current_affirmation,
        'previous_affirmations': previous_affirmations,
    }
    
    return render(request, 'quotes/daily_affirmations.html', context)


def blog(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'quotes/blog.html', {'posts': posts})


def subscription_success(request):
    return render(request, 'quotes/subscription_success.html')


# Views for custom admin interface
@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def manage_affirmations(request):
    affirmations = DailyAffirmation.objects.all()
    return render(request, 'dashboard/manage_affirmations.html', {'affirmations': affirmations})

@login_required
def add_affirmation(request):
    if request.method == "POST":
        form = DailyAffirmationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_affirmations')
    else:
        form = DailyAffirmationForm()
    return render(request, 'dashboard/add_affirmation.html', {'form': form})

@login_required
def edit_affirmation(request, pk):
    affirmation = get_object_or_404(DailyAffirmation, pk=pk)
    if request.method == "POST":
        form = DailyAffirmationForm(request.POST, instance=affirmation)
        if form.is_valid():
            form.save()
            return redirect('manage_affirmations')
    else:
        form = DailyAffirmationForm(instance=affirmation)
    return render(request, 'dashboard/edit_affirmation.html', {'form': form})

@login_required
def delete_affirmation(request, pk):
    affirmation = get_object_or_404(DailyAffirmation, pk=pk)
    if request.method == "POST":
        affirmation.delete()
        return redirect('manage_affirmations')
    return render(request, 'dashboard/delete_affirmation.html', {'affirmation': affirmation})

@login_required
def manage_blogs(request):
    blogs = BlogPost.objects.all()
    return render(request, 'dashboard/manage_blogs.html', {'blogs': blogs})

@login_required
def add_blog(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_blogs')
    else:
        form = BlogPostForm()
    return render(request, 'dashboard/add_blog.html', {'form': form})

@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('manage_blogs')
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'dashboard/edit_blog.html', {'form': form})

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        blog.delete()
        return redirect('manage_blogs')
    return render(request, 'dashboard/delete_blog.html', {'blog': blog})

@login_required
def manage_subscribers(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'dashboard/manage_subscribers.html', {'subscribers': subscribers})