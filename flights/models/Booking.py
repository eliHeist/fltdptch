from django.db import models


class Booking(models.Model):
    reference = models.CharField(max_length=20, unique=True)
    person_count = models.PositiveSmallIntegerField()
    date = models.DateField(null=True)

    def __str__(self):
        return self.reference
