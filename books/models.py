from django.db import models


# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    first_publish_year = models.IntegerField()
    first_sentence = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.title


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookreviews')
    review_title = models.CharField(max_length=255)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review_title
