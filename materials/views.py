from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from users.permissions import IsModers


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        else:
            return CourseSerializer

    def perform_create(self, serializer):
        """Пользователь-создатель=владелец"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """ Проверка прав пользователя - модератор может только изменять и просматривать курсы"""
        if self.action in ['create', 'destroy']:
            self.permission_classes = (~IsModers,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModers,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Пользователь-создатель=владелец"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
