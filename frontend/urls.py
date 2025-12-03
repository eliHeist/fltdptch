from django.urls import path
from .views import flights

app_name = "frontend"

urlpatterns = [
    path("flights/", flights.FlightListView.as_view(), name="flights"),
]