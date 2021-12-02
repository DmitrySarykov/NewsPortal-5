from django.urls import path, include
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('news/', include('news.urls')),
]