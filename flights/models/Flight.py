from django.db import models


class Flight(models.Model):
    date = models.DateField()
    flight_number = models.CharField(max_length=10)
    aircraft = models.ForeignKey("flights.Aircraft", on_delete=models.SET_NULL, null=True)

    opening_counters = models.TimeField(null=True, blank=True)
    closing_counters = models.TimeField(null=True, blank=True)
    boarding_bus = models.TimeField(null=True, blank=True)
    arrival_at_aircraft = models.TimeField(null=True, blank=True)

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
        related_name="dispatch_flights"
    )

    supervisor = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="supervised_flights"
    )

    supervisor_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("date", "flight_number")

    def __str__(self):
        return f"{self.date} {self.flight_number}"
    
    supervisor_status = lambda self: "Closed" if self.supervisor_closed else "Open"
