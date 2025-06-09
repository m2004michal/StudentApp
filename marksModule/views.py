import csv

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from marksModule.models import MarkModel
from marksModule.serializers.MarkSerializer import MarkSerializer
from marksModule.service.MarksService import add_mark, delete_mark


class AddMarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = MarkSerializer(data=request.data)
        if serializer.is_valid():
            mark = add_mark(
                user=request.user,
                subject_name=serializer.validated_data['subject_name'],
                grade=serializer.validated_data['grade'],
                date=serializer.validated_data['date']
            )
            return Response(MarkSerializer(mark).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteMarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, mark_id):
        try:
            delete_mark(user=request.user, mark_id=mark_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({"detail": "Not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

class MarkListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        marks = MarkModel.objects.filter(user=request.user).order_by('-date')
        serializer = MarkSerializer(marks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExportMarksCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        marks = MarkModel.objects.filter(user=request.user).order_by("date")
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="dziennik_ocen.csv"'

        writer = csv.writer(response)
        writer.writerow(["Data", "Przedmiot", "Ocena"])

        for mark in marks:
            writer.writerow([
                mark.date,
                mark.subject_name,
                mark.grade
            ])
        return response
