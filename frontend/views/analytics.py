from collections import Counter, OrderedDict
from datetime import timedelta, date
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.dateparse import parse_date

from flights.models import Flight

User = get_user_model()


def quarter_start(d: date) -> date:
    q = (d.month - 1) // 3
    start_month = q * 3 + 1
    return date(d.year, start_month, 1)


class AnalyticsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        today = timezone.localtime(timezone.now()).date()
        print("Today:", today)

        # Parse period and optional custom start/end
        period = request.GET.get("period", "this_week")
        start = None
        end = None

        if period == "today":
            start = end = today
        elif period == "this_week":
            # week starts Monday
            start = today - timedelta(days=today.weekday())
            end = today
        elif period == "this_month":
            start = date(today.year, today.month, 1)
            end = today
        elif period == "this_quarter":
            start = quarter_start(today)
            end = today
        elif period == "custom":
            # Expect start and end as YYYY-MM-DD
            s = request.GET.get("start")
            e = request.GET.get("end")
            try:
                start = parse_date(s) if s else None
                end = parse_date(e) if e else None
            except Exception:
                start = end = None

        # Fallback: default to this week if no range determined
        if not start and not end:
            start = today - timedelta(days=today.weekday())
            end = today

        # Normalize end if missing
        if start and not end:
            end = start
        if end and not start:
            start = end

        print(start, end)

        # Filter flights in inclusive date range
        flights_qs = Flight.objects.filter(date__lte=today)
        if start:
            flights_qs = flights_qs.filter(date__gte=start)
        if end:
            flights_qs = flights_qs.filter(date__lte=end)

        flights = flights_qs.order_by("-date", "flight_number")

        grouped_data = OrderedDict()
        stats_data = {
            "users": {},
            "overall": {"total_flights": flights.count(), "unique_aircraft": 0},
        }
        aircrafts_data = {}

        aircraft_set = set()

        for flight in flights:
            date_key = flight.date
            if date_key not in grouped_data:
                grouped_data[date_key] = {
                    "flights": [],
                    "count": 0,
                    "aircraft_counts": Counter(),
                }

            grouped_data[date_key]["flights"].append(flight)
            grouped_data[date_key]["count"] += 1

            if flight.aircraft:
                reg = flight.aircraft.reg
                aircrafts_data.setdefault(flight.aircraft.pk, {"aircraft": flight.aircraft, "flight_count": 0})
                aircrafts_data[flight.aircraft.pk]["flight_count"] += 1
            else:
                reg = "(unknown)"

            grouped_data[date_key]["aircraft_counts"][reg] += 1
            aircraft_set.add(reg)

            counter = flight.counters_by
            dispatcher = flight.dispatched_by

            if counter:
                stats_data["users"].setdefault(counter, {"counters_count": 0, "dispatches_count": 0})
                stats_data["users"][counter]["counters_count"] += 1

            if dispatcher:
                stats_data["users"].setdefault(dispatcher, {"counters_count": 0, "dispatches_count": 0})
                stats_data["users"][dispatcher]["dispatches_count"] += 1

        stats_data["overall"]["unique_aircraft"] = len(aircraft_set)

        # Convert aircraft_counts Counters to regular dicts for template friendliness
        for date_key, data in grouped_data.items():
            data["aircraft_counts"] = dict(data["aircraft_counts"])

        context = {
            "grouped_data": grouped_data,
            "stats_data": stats_data,
            "aircrafts_data": aircrafts_data,
            "period": period,
            "start": start,
            "end": end,
        }

        return render(request, "frontend/analytics/base.html", context)
    