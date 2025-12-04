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
        # create flight groups per date

        context = {
            "flights": flights,
            "aircrafts": aircrafts,
            "date": date,
        }
        
        return render(request, "frontend/flights/planning-center.html", context)
    
    def post(self, request, *args, **kwargs):
        date_str = request.POST.get("date")
        date = parse_date(date_str)

        # flights come as rows: flight_number, aircraft_id
        rows = int(request.POST.get("rows", 0))
        for i in range(rows):
            flight_number = request.POST.get(f"flight_number_{i}")
            aircraft_id = request.POST.get(f"aircraft_{i}")
            if flight_number and aircraft_id:
                Flight.objects.get_or_create(
                    date=date,
                    flight_number=flight_number,
                    aircraft_id=aircraft_id
                )

        return redirect("frontend:planning")