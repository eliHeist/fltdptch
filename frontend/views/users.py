from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db import transaction

from django.utils import timezone
from django.utils.dateparse import parse_date

from accounts.models import UserProfile
from flights.models import Aircraft, Flight

User = get_user_model()


class UsersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        date_str = request.GET.get("date")
        date = parse_date(date_str) if date_str else timezone.now().date()

        users = User.objects.filter(is_active=True).order_by("last_name")

        # aircraft_options = [{'value': f"{aircraft.id}", 'label': aircraft.full_name()} for aircraft in aircrafts]

        context = {
            "users": users,
            "date": date,
        }
        
        return render(request, "frontend/users/list.html", context)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        if action == "edit-user":
            self._edit_user(request)
        if action == "add-user":
            self._add_user(request)

        return redirect("frontend:users")
    
    def _add_user(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        identifier = request.POST.get("identifier")

        with transaction.atomic():
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                # password=User.objects.make_random_password(),
                password="Pwrd0987",
            )

            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.gender = gender
            user_profile.identifier = identifier
            user_profile.save()
    
    def _edit_user(self, request):
        pk = request.POST.get("pk")
        user = User.objects.get(pk=pk)

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        identifier = request.POST.get("identifier")

        with transaction.atomic():
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.gender = gender
            user_profile.identifier = identifier
            user_profile.save()
