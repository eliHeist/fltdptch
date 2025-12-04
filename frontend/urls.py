from django.urls import path
from .views import flights, planning, aircrafts, users

app_name = "frontend"

urlpatterns = [
    path("flights/", flights.FlightListView.as_view(), name="flights"),
    path("planning/", planning.PlanningView.as_view(), name="planning"),
    path("aircrafts/", aircrafts.AircraftsListView.as_view(), name="aircrafts"),
    path("users/", users.UsersView.as_view(), name="users"),
]