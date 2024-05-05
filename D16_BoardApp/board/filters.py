from django_filters import FilterSet
from .models import Response

class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = ['advertisement']  # Указываем поле, по которому будем фильтровать