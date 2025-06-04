from django.db import models

from authentication.models import User


class DailySchedule(models.Model):
    Date = models.DateField(null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_schedules')

