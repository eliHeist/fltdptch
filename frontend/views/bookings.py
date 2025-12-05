from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.dateparse import parse_date

from flights.models import Booking


class BookingsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.all().order_by("-date", "reference")

        context = {
            "bookings": bookings,
        }
        
        return render(request, "frontend/bookings/list.html", context)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        if action == "add-booking":
            date_str = request.POST.get("date")
            date = parse_date(date_str) if date_str else timezone.localtime(timezone.now()).date()
            
            reference = request.POST.get("reference")
            person_count = request.POST.get("person_count")

            if not reference:
                return redirect("frontend:bookings")
            
            Booking.objects.get_or_create(
                date=date,
                reference=reference, 
                person_count=person_count,
            )
            return redirect("frontend:bookings")
        
        elif action == "edit-booking":
            pk = request.POST.get("pk")
            date_str = request.POST.get("date")
            date = parse_date(date_str) if date_str else timezone.localtime(timezone.now()).date()
            
            reference = request.POST.get("reference")
            person_count = request.POST.get("person_count")

            if not reference:
                return redirect("frontend:bookings")
            
            booking = Booking.objects.get(pk=pk)
            if reference:
                booking.reference = reference
            if person_count:
                booking.person_count = person_count
            if date:
                booking.date = date
            booking.save()
            return redirect("frontend:bookings")