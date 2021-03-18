from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from news.models import Article, Category


class ArticleAdminForm(forms.ModelForm):
    def clean_categories(self):
        data = self.cleaned_data['categories']
        if len(data) > 3:
            raise ValidationError('No more than 3 categories allowed!')
        return data


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
