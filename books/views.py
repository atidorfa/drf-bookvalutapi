from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from .models import Book


class BookInfoView(APIView):
    def get(self, request):
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
