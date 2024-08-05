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

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    fields = ('title', 'content', 'image')

admin.site.register(BlogPost, BlogPostAdmin)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    list_filter = ('subscribed_at',)