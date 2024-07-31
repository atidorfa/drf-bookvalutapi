from rest_framework import serializers
from .models import BookReview


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ["id", 'isbn', 'title', 'comment', 'date_created']
        read_only_fields = ['date_created']
