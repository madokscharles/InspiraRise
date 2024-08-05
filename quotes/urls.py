from django.urls import path
from .views import (
    quote_view, daily_affirmations, blog, subscription_success,
    dashboard, manage_affirmations, add_affirmation, edit_affirmation, delete_affirmation,
    manage_blogs, add_blog, edit_blog, delete_blog, manage_subscribers
)

urlpatterns = [
    path('', quote_view, name='home'),
    path('daily-affirmations/', daily_affirmations, name='daily_affirmations'),
    path('blog/', blog, name='blog'),
    path('subscription-success/', subscription_success, name='subscription_success'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/affirmations/', manage_affirmations, name='manage_affirmations'),
    path('dashboard/affirmations/add/', add_affirmation, name='add_affirmation'),
    path('dashboard/affirmations/edit/<int:pk>/', edit_affirmation, name='edit_affirmation'),
    path('dashboard/affirmations/delete/<int:pk>/', delete_affirmation, name='delete_affirmation'),
    path('dashboard/blogs/', manage_blogs, name='manage_blogs'),
    path('dashboard/blogs/add/', add_blog, name='add_blog'),
    path('dashboard/blogs/edit/<int:pk>/', edit_blog, name='edit_blog'),
    path('dashboard/blogs/delete/<int:pk>/', delete_blog, name='delete_blog'),
    path('dashboard/subscribers/', manage_subscribers, name='manage_subscribers'),
]
