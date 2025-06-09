from rest_framework import serializers

from scheduleModule.models import DailySchedule
from scheduleModule.serializers.task_serializer import TaskSerializer


class DailyScheduleSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = DailySchedule
        fields = ['id', 'Date', 'user', 'tasks']