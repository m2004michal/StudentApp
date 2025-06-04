from django.db import models
from rest_framework.exceptions import ValidationError


class Task(models.Model):
    schedule = models.ForeignKey('DailySchedule', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.title} ({self.start_time}-{self.end_time})"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

        overlapping = Task.objects.filter(
            schedule=self.schedule,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("Zajecia pokrywaja sie z innymi.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.clean()
        super().delete(*args, **kwargs)