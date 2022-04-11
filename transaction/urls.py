from django.urls import path, include

from transaction.views import PaypalView


urlpatterns = [
    path('paypal/', PaypalView.as_view())

]
