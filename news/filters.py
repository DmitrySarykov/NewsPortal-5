from django.db.models.fields.related import ForeignKey
from django_filters import FilterSet 
from .models import Post
 
class SearchFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'date': ['gt'],
            'author':['exact'],
            'category':['exact'],    
        }