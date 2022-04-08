from django.urls import path, include
from . import views


urlpatterns = [
    path('state_list/', views.US_StateListView.as_view()),
    path('list_state/', views.US_StateListView.as_view()),
    path('states/', views.US_StateWithCityLlistView.as_view()),
    path('states/<str:state_code>', views.US_StateWithCityDetailView.as_view())

]
