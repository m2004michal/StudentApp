
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import RegisterView, CustomLoginView, LogoutView
from scheduleModule.views import DailyScheduleByDateView, DailyScheduleAutoCreateView, TaskCreateView, TaskDeleteView, \
    ExportScheduleCSVView
from marksModule.views import DeleteMarkView, AddMarkView, MarkListView, ExportMarksCSVView, MarkStatisticsView, \
    ExportStatisticsCSVView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('daily-schedule/<str:date_str>/', DailyScheduleByDateView.as_view(), name='daily-schedule-by-date'),
    path('daily-schedule/create-if-needed/<str:date_str>/', DailyScheduleAutoCreateView.as_view(),
         name='daily-schedule-get-or-create'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/delete/<int:id>', TaskDeleteView.as_view(), name='task-delete'),
    path('marks/add/', AddMarkView.as_view(), name='add-mark'),
    path('marks/delete/<int:mark_id>/', DeleteMarkView.as_view(), name='delete-mark'),
    path("marks/", MarkListView.as_view(), name="marks-list"),
    path("export/schedule/", ExportScheduleCSVView.as_view(), name="export-schedule"),
    path("export/marks/", ExportMarksCSVView.as_view(), name="export-marks"),
    path("marks/statistics/", MarkStatisticsView.as_view(), name="mark-statistics"),
    path("marks/statistics/export/", ExportStatisticsCSVView.as_view(), name="mark-statistics-export"),



]
