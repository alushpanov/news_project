from django import forms

from news.models import Category


class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Title"
        })
    )
    article_text = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Article content"
        })
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False
    )
    image = forms.ImageField(
        required=False
        # widget=forms.ClearableFileInput()
    )
