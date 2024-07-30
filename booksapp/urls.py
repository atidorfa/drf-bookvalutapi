from rest_framework.routers import DefaultRouter
from .api import BookReviewViewSet


router = DefaultRouter()
router.register('api/books', BookReviewViewSet, 'books')
urlpatterns = router.urls
