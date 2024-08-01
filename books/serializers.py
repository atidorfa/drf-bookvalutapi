from rest_framework import serializers
from .models import Book, BookReview


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'first_publish_year', 'first_sentence']


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ['book', 'review_title', 'comment', 'date_created']
        read_only_fields = ['date_created']
