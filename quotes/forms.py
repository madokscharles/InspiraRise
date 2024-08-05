from django import forms
from .models import Category, Subscriber, DailyAffirmation, BlogPost

class QuoteForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label='Random')

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']

class DailyAffirmationForm(forms.ModelForm):
    class Meta:
        model = DailyAffirmation
        fields = ['text']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
