from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from django.utils import timezone
from django.utils.dateparse import parse_date

from flights.models import Flight, Reconfirmation

class LandingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        date = timezone.localtime(timezone.now()).date()
        user = request.user

        flights = user.assigned_flights.filter(date=date).order_by("flight_number")
        pending_reconfirmations = user.reconfirmations.filter(date_for__gte=date)

        context = {
            "flights": flights,
            "pending_reconfirmations": pending_reconfirmations,
        }
        
        return render(request, 'frontend/landing/landing.html', context)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")

        if action == "reconfirm":
            pk = request.POST.get("pk")
            reconfirmation = Reconfirmation.objects.get(pk=pk)
            reconfirmation.date_sent = timezone.localtime(timezone.now()).date()
            reconfirmation.save()
        
        return self.get(request, *args, **kwargs)
