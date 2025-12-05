from django.db import models


class Flight(models.Model):
    date = models.DateField()
    flight_number = models.CharField(max_length=10)
    aircraft = models.ForeignKey("flights.Aircraft", on_delete=models.SET_NULL, null=True)

    opening_counters = models.TimeField(null=True, blank=True)
    closing_counters = models.TimeField(null=True, blank=True)
    boarding_bus = models.TimeField(null=True, blank=True)
    arrival_at_aircraft = models.TimeField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_flights"
    )

    counters_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="counter_flights"
    )

    dispatched_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="dispatched_flights"
    )

    supervisor = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="supervised_flights"
    )

    class Status(models.IntegerChoices):
        OPEN = 0, "Open"
        DISPATCHED = 1, "Dispatched"

    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.OPEN)

    class Meta:
        unique_together = ("date", "flight_number")

    def __str__(self):
        return f"{self.date} {self.flight_number}"
    
    # Lambdas for formatted output
    opening_counters_fmt = lambda self: self.opening_counters.strftime("%H:%M") if self.opening_counters else "-"
    closing_counters_fmt = lambda self: self.closing_counters.strftime("%H:%M") if self.closing_counters else "-"
    boarding_bus_fmt = lambda self: self.boarding_bus.strftime("%H:%M") if self.boarding_bus else "-"
    arrival_at_aircraft_fmt = lambda self: self.arrival_at_aircraft.strftime("%H:%M") if self.arrival_at_aircraft else "-"

    counter_id = lambda self: self.counters_by_id or self.assigned_to_id
    dispatcher_id = lambda self: self.dispatched_by_id or self.assigned_to_id

    ready_for_dispatch = lambda self: all([
        self.opening_counters is not None,
        self.closing_counters is not None,
        self.boarding_bus is not None,
        self.arrival_at_aircraft is not None,
    ])