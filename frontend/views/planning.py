from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from django.utils import timezone
from django.utils.dateparse import parse_date

from flights.models import Aircraft, Flight, Reconfirmation

User = get_user_model()

class PlanningView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        date_str = request.GET.get("date")
        date = parse_date(date_str) if date_str else timezone.localtime(timezone.now()).date()

        flights = Flight.objects.filter(date=date).order_by("date", "flight_number")
        aircrafts = Aircraft.objects.all()
        users = User.objects.filter(is_active=True).order_by("last_name", "first_name")

        # {'value': aircraft.id, 'label': aircraft.full_name}
        aircraft_options = [{'value': f"{aircraft.id}", 'label': aircraft.full_name()} for aircraft in aircrafts]

        user_options = [{'value': f"{user.id}", 'label': user.get_name()} for user in users]

        reconfirmation = Reconfirmation.objects.filter(date_for=date).first()

        print(reconfirmation.assignees.all())
        
        selected_users = [str(uid) for uid in reconfirmation.assignees.all().values_list('id', flat=True)] if reconfirmation else []

        context = {
            "flights": flights,
            "aircraft_options": aircraft_options,
            "user_options": user_options,
            "date": date,
            "selected_users": list(selected_users),
            "reconfirmation": reconfirmation,
        }
        
        return render(request, "frontend/flights/planning-center.html", context)
    
    def post(self, request, *args, **kwargs):
        date_str = request.GET.get("date")
        date = parse_date(date_str) if date_str else timezone.localtime(timezone.now()).date()

        print(args)

        base_url = reverse("frontend:planning")
        query_string = urlencode({"date": date.strftime("%Y-%m-%d")})
        url = f"{base_url}?{query_string}"

        action = request.POST.get("action")

        if action == "add-flight":
            flight_number = request.POST.get("flight_number")
            aircraft_id = request.POST.get("aircraft_id")
            assignee_id = request.POST.get("assignee_id")

            if not flight_number or not aircraft_id or not assignee_id:
                print("missing flight number, aircraft ID, or assignee ID")
                return redirect(url)
            try:
                aircraft = Aircraft.objects.get(id=aircraft_id)
                assignee = User.objects.get(pk=assignee_id)
                flight, created = Flight.objects.get_or_create(
                    date=date,
                    flight_number=flight_number,
                    aircraft=aircraft,
                    assigned_to=assignee,
                )
            except Aircraft.DoesNotExist:
                print("invalid ID")
                pass
        
        elif action == "edit-flight":
            pk = request.POST.get("pk")
            flight = Flight.objects.get(pk=pk)

            flight_number = request.POST.get("flight_number")
            aircraft_id = request.POST.get("aircraft_id")
            assignee_id = request.POST.get("assignee_id")

            if flight_number:
                flight.flight_number = flight_number
            if aircraft_id:
                try:
                    aircraft = Aircraft.objects.get(id=aircraft_id)
                    flight.aircraft = aircraft
                except Aircraft.DoesNotExist:
                    print("invalid aircraft ID")
                    pass
            if assignee_id:
                try:
                    assignee = User.objects.get(pk=assignee_id)
                    flight.assigned_to = assignee
                except User.DoesNotExist:
                    print("invalid assignee ID")
                    pass
            flight.save()

        elif action == "set-reconfirmation-assignees":
            assignee_ids = request.POST.getlist("assignee_ids")
            print()
            reconfirmation, created = Reconfirmation.objects.get_or_create(date_for=date)
            assignees = User.objects.filter(id__in=assignee_ids)
            reconfirmation.assignees.set(assignees)
        
        return redirect(url)