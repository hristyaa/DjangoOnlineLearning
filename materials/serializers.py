from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
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
