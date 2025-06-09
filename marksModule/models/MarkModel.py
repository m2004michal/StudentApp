from django.db import models
from authentication.models import User


class MarkModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marks')
    subject_name = models.CharField(max_length=100)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.subject_name} - {self.grade} ({self.user.email})"