from django import forms

from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'postCategory',
            'text',
        ]

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'postCategory',
            'text',
        ]