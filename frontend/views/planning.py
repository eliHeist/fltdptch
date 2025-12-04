from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from django.utils.dateparse import parse_date

from flights.models import Aircraft, Flight


class PlanningView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        date_str = request.GET.get("date")
        date = parse_date(date_str) if date_str else timezone.now().date()

        flights = Flight.objects.filter(date=date).order_by("date", "flight_number")
        aircrafts = Aircraft.objects.all()

        # {'value': aircraft.id, 'label': aircraft.full_name}
        aircraft_options = [{'value': f"{aircraft.id}", 'label': aircraft.full_name()} for aircraft in aircrafts]

        context = {
            "flights": flights,
            "aircraft_options": aircraft_options,
            "date": date,
        }
        
        return render(request, "frontend/flights/planning-center.html", context)
    
    def post(self, request, *args, **kwargs):
        date_str = request.POST.get("date")
        date = parse_date(date_str)

        action = request.POST.get("action")
        if action == "add-flight":
            flight_number = request.POST.get("flight_number")
            aircraft_id = request.POST.get("aircraft_id")

            if not flight_number or not aircraft_id:
                print("missing flight number or aircraft ID")
                return redirect("frontend:planning")
            try:
                aircraft = Aircraft.objects.get(id=aircraft_id)
                Flight.objects.get_or_create(
                    date=date,
                    flight_number=flight_number,
                    aircraft=aircraft,
                )
            except Aircraft.DoesNotExist:
                print("invalid ID")
                pass

        return redirect("frontend:planning")