from datetime import date
from authentication.models import User
from scheduleModule.models import DailySchedule


def get_daily_schedule_for_user_and_date(user: User, target_date: date) -> DailySchedule | None:
    try:
        return DailySchedule.objects.get(user=user, Date=target_date)
    except DailySchedule.DoesNotExist:
        return None

def get_or_create_daily_schedule_for_user_and_date(user: User, target_date: date) -> DailySchedule:
    schedule, _ = DailySchedule.objects.get_or_create(user=user, Date=target_date)
    return schedule