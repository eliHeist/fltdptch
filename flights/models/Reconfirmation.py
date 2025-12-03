from django.db import models


class Reconfirmation(models.Model):
    date_for = models.DateField()
    assignees = models.ManyToManyField("accounts.User")
    date_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.date_for)
    
