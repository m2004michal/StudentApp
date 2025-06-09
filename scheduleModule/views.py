import csv
from datetime import datetime

from django.http import HttpResponse
from django.views.generic import DeleteView
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView

from marksModule.models import MarkModel
from marksModule.serializers.MarkSerializer import MarkSerializer
from scheduleModule.models import DailySchedule
from scheduleModule.models.task_models import Task
from scheduleModule.serializers.daily_schedule_serializer import DailyScheduleSerializer
from scheduleModule.serializers.task_serializer import TaskSerializer
from scheduleModule.services.daily_schedule_service import get_daily_schedule_for_user_and_date, \
    get_or_create_daily_schedule_for_user_and_date


class DailyScheduleByDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, date_str):
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': 'Zły format daty. Użyj YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        schedule = get_daily_schedule_for_user_and_date(request.user, target_date)
        if schedule:
            serializer = DailyScheduleSerializer(schedule)
            return Response(serializer.data)
        else:
            return Response({'error': 'Brak harmonogramu dla podanej daty.'}, status=status.HTTP_404_NOT_FOUND)


class DailyScheduleAutoCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, date_str):
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': 'Zły format daty. Użyj YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        schedule = get_or_create_daily_schedule_for_user_and_date(request.user, target_date)
        serializer = DailyScheduleSerializer(schedule)
        return Response(serializer.data)

class TaskCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(schedule__user=self.request.user)


class ExportScheduleCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        schedules = DailySchedule.objects.filter(user=request.user).prefetch_related("tasks")
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="plan_zajec.csv"'

        writer = csv.writer(response)
        writer.writerow(["Data", "Tytuł", "Godzina rozpoczęcia", "Godzina zakończenia", "Lokalizacja"])

        for schedule in schedules:
            for task in schedule.tasks.all():
                writer.writerow([
                    schedule.Date,
                    task.title,
                    task.start_time,
                    task.end_time,
                    task.location,
                ])
        return response