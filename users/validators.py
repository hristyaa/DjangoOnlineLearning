from rest_framework.serializers import ValidationError


def validate_paid_course_or_lesson(paid_course, paid_lesson):
    """Валидация: либо курс, либо урок"""
    if paid_course and paid_lesson:
        raise ValidationError("Укажите для оплаты что-то одно: либо курс, либо урок")
    if not paid_course and not paid_lesson:
        raise ValidationError("Необходимо указать либо курс, либо урок для оплаты")
