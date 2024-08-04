from django import forms
from .models import Category

class QuoteForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label='Random')
