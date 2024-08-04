from django.contrib import admin
from .models import Category, Quote, DailyAffirmation, BlogPost, Subscriber

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'category')

# Register DailyAffirmation and BlogPost models
admin.site.register(DailyAffirmation)
admin.site.register(BlogPost)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    list_filter = ('subscribed_at',)