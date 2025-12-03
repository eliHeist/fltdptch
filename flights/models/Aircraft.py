from django.db import models


class Aircraft(models.Model):
    reg = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.reg
