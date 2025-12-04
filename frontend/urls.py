from django.urls import path
from .views import flights, planning

app_name = "frontend"

urlpatterns = [
    path("flights/", flights.FlightListView.as_view(), name="flights"),
    path("planning/", planning.PlanningView.as_view(), name="planning"),
]