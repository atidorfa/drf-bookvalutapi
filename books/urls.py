from django.urls import path
from .views import BookInfoView


urlpatterns = [
    path('book-info/', BookInfoView.as_view(), name='book-info'),
]
