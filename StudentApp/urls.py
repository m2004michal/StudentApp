
from django.urls import path
from authentication.views import RegisterView, CustomLoginView, LogoutView
from scheduleModule.views import DailyScheduleByDateView, DailyScheduleAutoCreateView, TaskCreateView, TaskDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('daily-schedule/<str:date_str>/', DailyScheduleByDateView.as_view(), name='daily-schedule-by-date'),
    path('daily-schedule/create-if-needed/<str:date_str>/', DailyScheduleAutoCreateView.as_view(),
         name='daily-schedule-get-or-create'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/delete/<int:id>', TaskDeleteView.as_view(), name='task-delete'),



]
