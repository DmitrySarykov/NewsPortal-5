from django.forms import ModelForm, Textarea, CharField
from .models import *

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['date','author', 'type', 'category', 'title', 'text', 'rating']