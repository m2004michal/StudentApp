from rest_framework import serializers
from scheduleModule.models.task_models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):
        schedule = data['schedule']
        start_time = data['start_time']
        end_time = data['end_time']

        if start_time >= end_time:
            raise serializers.ValidationError("Start time must be before end time.")

        overlapping = Task.objects.filter(
            schedule=schedule,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        if self.instance:
            overlapping = overlapping.exclude(id=self.instance.id)

        if overlapping.exists():
            raise serializers.ValidationError("Zajecia pokrywaja sie z innymi.")

        return data