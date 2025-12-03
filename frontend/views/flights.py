from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from django.utils.dateparse import parse_date

from flights.models import Flight


class FlightListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        date_str = request.GET.get("date")
        date = timezone.now().date() if not date_str else parse_date(date_str)
        flights = Flight.objects.filter(date=date).order_by("date", "flight_number")

        context = {
            "flights": flights,
            "date": date,
        }
        
        return render(request, "flights/flight_list.html", context)
