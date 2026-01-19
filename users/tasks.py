from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_users_by_last_login():
    """
    Проверка пользователей по дате последнего входа по полю last_login;
    если пользователь не заходил более месяца, блокирует его с помощью флага is_active
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    users = User.objects.filter(
        last_login__lt=one_month_ago, is_active=True, last_login__isnull=False
    )
    users.update(is_active=False)
