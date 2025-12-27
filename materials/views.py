from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from users.permissions import IsModers, IsOwner


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
        """
        Проверка прав пользователя:
        Модератор может просматривать и редактировать любые уроки и курсы, но не может удалять и создавать уроки и курсы.
        Пользователи, которые не входят в группу модераторов, могли видеть, редактировать и удалять только свои курсы и уроки.
        """
        if self.action == "create":
            self.permission_classes = (~IsModers,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModers | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | ~IsModers,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (
        ~IsModers,
        IsAuthenticated,
    )

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
    permission_classes = (
        IsAuthenticated,
        IsModers | IsOwner,
    )


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModers | IsOwner,
    )


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsOwner | ~IsModers,
    )
