from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('customer', views.CustomerViewSet)
router.urls

urlpatterns = router.urls
