from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet

router = DefaultRouter()
router.register('image2sketch', ImageViewSet, basename='image2sketch')

urlpatterns = router.urls

