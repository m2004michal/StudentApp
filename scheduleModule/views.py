from datetime import datetime

from django.views.generic import DeleteView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView

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

