from django.db import models
from django.conf import settings

from authentication.models import User


class DailySchedule(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_schedules')
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    tasks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.day_of_week} ({self.start_time}-{self.end_time})"


class WeeklySchedule(models.Model):
    week_start_date = models.DateField(null=True, blank=True, default=None)
    week_end_date = models.DateField(null=True, blank=True, default=None)
    monday = models.OneToOneField(DailySchedule, on_delete=models.CASCADE, related_name='monday_schedule')
    tuesday = models.OneToOneField(DailySchedule, on_delete=models.CASCADE, related_name='tuesday_schedule')
    wednesday = models.OneToOneField(DailySchedule, on_delete=models.CASCADE, related_name='wednesday_schedule')
    thursday = models.OneToOneField(DailySchedule, on_delete=models.CASCADE, related_name='thursday_schedule')
    friday = models.OneToOneField(DailySchedule, on_delete=models.CASCADE, related_name='friday_schedule')
    saturday = models.OneToOneField(DailySchedule, on_delete=models.CASCADE, related_name='saturday_schedule')
    sunday = models.OneToOneField(DailySchedule, on_delete=models.CASCADE, related_name='sunday_schedule')

    def __str__(self):
        return f"Schedule for {self.user.username}"