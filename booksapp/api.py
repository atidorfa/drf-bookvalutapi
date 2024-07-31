from .models import BookReview
from .serializers import BookReviewSerializer
from rest_framework import viewsets, permissions

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BookReview
from .serializers import BookReviewSerializer


class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BookReviewSerializer

    def list(self, request, *args, **kwargs):
        isbn = request.query_params.get('isbn')

        if isbn:
            # If ISBN is provided in the query params, filter the queryset
            try:
                book = self.queryset.get(isbn=isbn)
                serializer = self.get_serializer(book)
                return Response(serializer.data)
            except BookReview.DoesNotExist:
                return Response(
                    {"error": "Book not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If no ISBN is provided, return the full list
        return super().list(request, *args, **kwargs)
