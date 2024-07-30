from django.db import models
from django.contrib.auth.models import User


class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
