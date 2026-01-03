from django.core.validators import URLValidator
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        """Метод для определения наличия/отсутствия подписки"""
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода количества и информации об уроках в курсе"""

    count_lessons = SerializerMethodField()
    lessons = SerializerMethodField()

    def get_count_lessons(self, course):
        return course.lessons.count()

    def get_lessons(self, course):
        lessons = Lesson.objects.filter(course=course)
        return [
            {
                "id": lesson.id,
                "name": lesson.name,
                "description": lesson.description,
            }
            for lesson in lessons
        ]

    class Meta:
        model = Course
        fields = ("name", "description", "count_lessons", "lessons")
