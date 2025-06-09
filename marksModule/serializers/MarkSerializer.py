from rest_framework import serializers

from marksModule.models import MarkModel


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkModel
        fields = ['id', 'subject_name', 'grade', 'date']
