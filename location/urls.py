from django.urls import path
from . import views


urlpatterns = [
    path('states/', views.US_StateListView.as_view()),
    path('states_and_cities/', views.US_StateWithCityLlistView.as_view()),
    path('states/<str:state_code>/',
         views.US_StateWithCityDetailView.as_view(), name='states__state_code')

]
