from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('customers', views.CustomerViewSet, basename='customers')

customer_router = routers.NestedDefaultRouter(
    router, 'customers', lookup='customer')
# customer_router.register(
#     'images', views.CutomerImageViewSet, basename='customer-images')


urlpatterns = router.urls + customer_router.urls
