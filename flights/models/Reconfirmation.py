from django.db import models


class Reconfirmation(models.Model):
    date_for = models.DateField(unique=True)
    assignees = models.ManyToManyField("accounts.User", related_name="reconfirmations")
    date_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.date_for)
    
    status = lambda self: [0, "Sent"] if self.date_sent else [1, "Pending"]
    
