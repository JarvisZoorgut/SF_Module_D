from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter, CharFilter
from django import forms
from .models import Post, Category


class PostFilter(FilterSet):
    title = CharFilter(lookup_expr='iregex', label='Название', widget=forms.TextInput(attrs={'placeholder': 'Введите название'}))
    dateCreation = DateTimeFilter(widget=forms.DateTimeInput(attrs={'type': 'date'}), label='Дата публикации (позже)', lookup_expr='gt')
    category = ModelMultipleChoiceFilter(field_name = 'postCategory', queryset = Category.objects.all(), label = 'Категория', conjoined = False)
