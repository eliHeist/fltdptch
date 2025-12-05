from django.urls import path
from .views import flights, planning, aircrafts, users, analytics, bookings, landing

app_name = "frontend"

urlpatterns = [
    path("", landing.LandingView.as_view(), name="landing"),
    path("flights/", flights.FlightListView.as_view(), name="flights"),
    path("planning/", planning.PlanningView.as_view(), name="planning"),
    path("aircrafts/", aircrafts.AircraftsListView.as_view(), name="aircrafts"),
    path("users/", users.UsersView.as_view(), name="users"),
    path("analytics/", analytics.AnalyticsView.as_view(), name="analytics"),
    path("bookings/", bookings.BookingsView.as_view(), name="bookings"),
]