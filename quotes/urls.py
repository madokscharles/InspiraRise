from django.urls import path
from .views import quote_view, daily_affirmations, blog, subscription_success

urlpatterns = [
    path('', quote_view, name='home'),
    path('daily-affirmations/', daily_affirmations, name='daily_affirmations'),
    path('blog/', blog, name='blog'),
    path('subscription-success/', subscription_success, name='subscription_success'),
]
