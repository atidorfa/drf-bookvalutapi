from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
import datetime
from .models import Book, BookReview
from .serializers import BookReviewSerializer
from rest_framework.exceptions import NotAuthenticated


class BookInfoView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):

        token = request.COOKIES.get('jwt')
        if not token:
            raise NotAuthenticated('Unauthenticated!')

        isbn = request.query_params.get('isbn')
        if not isbn:
            return Response({"error": "ISBN query parameter is required."}, status=400)

        # Try to fetch book info from internal DATABASE
        try:
            book = Book.objects.get(isbn=isbn)
            return Response({
                'message': 'success',
                'book': {
                    'isbn': book.isbn,
                    'title': book.title,
                    'author': book.author,
                    'first_publish_year': book.first_publish_year,
                    'first_sentence': book.first_sentence,
                }
            }, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            pass

        # Proceed to fetch from external API using AWS Lambda function via API GATEWAY
        url = "https://09evadfsw0.execute-api.us-east-1.amazonaws.com/dev"
        payload = {
            "body": json.dumps({"isbn": isbn})
        }

        try:
            response = requests.get(url, data=json.dumps(payload))
            response.raise_for_status()
            book_info = response.json()['body']

            # Ensure book_info is parsed correctly
            if isinstance(book_info, str):
                book_info = json.loads(book_info)

            # Assuming book_info contains the necessary fields, add book into db
            book = Book.objects.create(
                isbn=isbn,
                title=book_info['title'],
                author=book_info['author'],
                first_publish_year=book_info['first_publish_year'],
                first_sentence=book_info['first_sentence']
            )
            book.save()

            return Response({
                'message': 'success',
                'book': {
                    'isbn': book.isbn,
                    'title': book.title,
                    'author': book.author,
                    'first_publish_year': book.first_publish_year,
                    'first_sentence': book.first_sentence,
                }
            }, status=status.HTTP_201_CREATED)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterBookReviewView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise NotAuthenticated('Unauthenticated!')

        isbn = request.data.get('isbn')
        review_title = request.data.get('review_title')
        comment = request.data.get('comment')

        if not isbn or not review_title or not comment:
            return Response({"error": "ISBN, review title, and comment are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return Response({"error": "Book with the provided ISBN does not exist."}, status=status.HTTP_404_NOT_FOUND)

        review_data = {
            'book': book.id,
            'review_title': review_title,
            'comment': comment,
            'date_created': datetime.datetime.now()
        }
        serializer = BookReviewSerializer(data=review_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReviewsByISBNView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise NotAuthenticated('Unauthenticated!')

        isbn = request.query_params.get('isbn')
        if not isbn:
            return Response({"error": "ISBN query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return Response({"error": "Book with the provided ISBN does not exist."}, status=status.HTTP_404_NOT_FOUND)

        reviews = BookReview.objects.filter(book=book)
        serializer = BookReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
