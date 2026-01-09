from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Прикрепите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Модель платежа"""

    PAIMENT_METHOD_CHOICES = [("cash", "Наличные"), ("cashless", "Перевод на счет")]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )
    date_payed = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        "materials.Course",
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True,
        related_name="payments",
    )
    paid_lesson = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True,
        related_name="payments",
    )
    payment_amount = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Сумма оплаты"
    )  # сумма оплаты берется из курса/урока
    payment_method = models.CharField(
        max_length=50,
        choices=PAIMENT_METHOD_CHOICES,
        default="cashless",
        verbose_name="Способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии оплаты",
        help_text="Укажите ID сессии оплаты",
    )
    link = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    def __str__(self):
        return f"{self.date_payed} - {self.payment_amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
