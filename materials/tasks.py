from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_email_about_update_course(email, title):
    """Отправка письма об обновлении курса"""
    send_mail(
        "Курс обновлен!",
        f"Материалы курса '{title}', на который Вы подписаны, обновлены.",
        EMAIL_HOST_USER,
        [email],
    )
