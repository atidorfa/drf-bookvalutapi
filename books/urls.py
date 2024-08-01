from django.urls import path
from .views import BookInfoView, RegisterBookReviewView, BookReviewsByISBNView


urlpatterns = [
    path('book-info/', BookInfoView.as_view(), name='book-info'),
    path('register-book-review/', RegisterBookReviewView.as_view(), name='register-book-review'),
    path('book-reviews/', BookReviewsByISBNView.as_view(), name='book-reviews-by-isbn')
]
