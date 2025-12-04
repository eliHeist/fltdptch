from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from flights.models import Aircraft


class AircraftsListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        aircrafts = Aircraft.objects.all()

        context = {
            "aircrafts": aircrafts,
        }
        
        return render(request, "frontend/aircrafts/list.html", context)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        if action == "add-aircraft":
            reg = request.POST.get("reg")

            if not reg:
                return redirect("frontend:aircrafts")
            reg = reg.upper()
            name = request.POST.get("name")
            Aircraft.objects.get_or_create(reg=reg, name=name)
            return redirect("frontend:aircrafts")
        
        elif action == "edit-aircraft":
            aircraft_id = request.POST.get("id")
            reg = request.POST.get("reg")
            if not aircraft_id or not reg:
                return redirect("frontend:aircrafts")
            reg = reg.upper()
            name = request.POST.get("name")
            try:
                aircraft = Aircraft.objects.get(id=aircraft_id)
                aircraft.reg = reg
                aircraft.name = name
                aircraft.save()
            except Aircraft.DoesNotExist:
                pass
            return redirect("frontend:aircrafts")