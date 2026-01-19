from django.core.management import BaseCommand

from users.models import User

# from django.utils import timezone
# from datetime import timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email="admin@mail.ru")
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.set_password("1234")
        user.save()


# создание пользователя для проверки задачи deactivate_users_by_last_login
#     def handle(self, *args, **options):
#         user = User.objects.create(email="block2@mail.ru")
#         user.is_active = True
#         user.last_login = timezone.now() - timedelta(days=31)
#         user.set_password("1234")
#         user.save()
