from marksModule.models import MarkModel
from django.shortcuts import get_object_or_404

def add_mark(user, subject_name, grade, date):
    return MarkModel.objects.create(user=user, subject_name=subject_name, grade=grade, date=date)

def delete_mark(user, mark_id):
    mark = get_object_or_404(MarkModel, id=mark_id, user=user)
    mark.delete()