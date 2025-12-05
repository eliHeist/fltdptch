from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from django.utils import timezone
from django.utils.dateparse import parse_date

from flights.models import Flight

User = get_user_model()

class FlightListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        date_str = request.GET.get("date")
        date = parse_date(date_str) if date_str else timezone.now().date()
        # flights = Flight.objects.filter(date=date).order_by("flight_number")
        flights = request.user.assigned_flights.filter(date=date).order_by("flight_number")

        users = User.objects.filter(is_active=True).order_by("last_name", "first_name")

        # {"value": pk, "label": "name"}
        user_options = [{"value": f"{user.pk}", "label": f"{user.get_name()}"} for user in users]

        context = {
            "flights": flights,
            "date": date,
            "user_options": user_options,
        }
        
        return render(request, "frontend/flights/list.html", context)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        pk = request.POST.get("pk")

        if action == "edit-counters":
            self._edit_counters(pk, request)
        if action == "dispatch-flight":
            self._dispatch_flight(pk, request)
        return redirect("frontend:flights")

    def _edit_counters(self, pk, request):
        flight = Flight.objects.get(pk=pk)
        opening_counters = request.POST.get("opening_counters")
        closing_counters = request.POST.get("closing_counters")
        boarding_bus = request.POST.get("boarding_bus")
        arrival_at_aircraft = request.POST.get("arrival_at_aircraft")

        flight.opening_counters = opening_counters or None
        flight.closing_counters = closing_counters or None
        flight.boarding_bus = boarding_bus or None
        flight.arrival_at_aircraft = arrival_at_aircraft or None
        flight.counters_by_id = request.user.pk
        flight.save()
    
    def _dispatch_flight(self, pk, request):
        flight = Flight.objects.get(pk=pk)
        counters_by_id = request.POST.get("counters_by_id")
        dispatched_by_id = request.POST.get("dispatched_by_id")
        flight.counters_by_id = counters_by_id
        flight.dispatched_by_id = dispatched_by_id
        flight.status = Flight.Status.DISPATCHED
        flight.save()