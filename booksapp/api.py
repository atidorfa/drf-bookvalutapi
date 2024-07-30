from .models import BookReview
from .serializers import BookReviewSerializer
from rest_framework import viewsets, permissions


class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BookReviewSerializer

