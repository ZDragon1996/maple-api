from django.urls import path, include
from . import views

urlpatterns = [
    path('states/', views.get_state),
    path('cities/', views.get_city)

]
