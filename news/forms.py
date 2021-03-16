from django import forms
from django.core.exceptions import ValidationError

from news.models import Category


class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Title"
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Content"
        })
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput()
    )

    def clean_categories(self):
        data = self.cleaned_data.get('categories')
        if len(data) > 3:
            raise ValidationError('No more than 3 categories allowed!')
        return data
