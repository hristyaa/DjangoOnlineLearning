from rest_framework.serializers import ValidationError


def validate_url(value):
    """Валидация ссылок (на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com)."""
    if not value.startswith("https://youtube.com"):
        raise ValidationError("Ссылка должна вести на видео с youtube.com")
