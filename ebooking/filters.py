import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class RoomFilter(django_filters.FilterSet):
    description = CharFilter(field_name='desctiption', lookup_expr='icontains')
    class Meta:
        model = Room
        fields = {
            'price': ['lt', 'gt'],
            'location' : ['exact']
        }