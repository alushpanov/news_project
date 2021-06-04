from django import forms
from django.core.exceptions import ValidationError

from news.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'categories', 'image']
        widgets = {
            'title': forms.TextInput(
                attrs={"placeholder": "Title"}
            ),
            'text': forms.Textarea(
                attrs={"placeholder": "Text"}
            ),
        }

    def clean_categories(self):
        data = self.cleaned_data.get('categories')
        if len(data) > 3:
            raise ValidationError('No more than 3 categories allowed!')
        return data


class ArticleAdminForm(ArticleForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'categories', 'image', 'author', 'views']
