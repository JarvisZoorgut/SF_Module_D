from django import forms
from .models import Advertisement, Response
from django_summernote.widgets import SummernoteWidget

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category']
        widgets = {
            'content': SummernoteWidget(),  # Заменяем стандартный виджет на SummernoteWidget
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
