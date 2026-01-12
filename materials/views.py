from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from users.permissions import IsModers, IsOwner


class CourseViewSet(ModelViewSet):
    """Viewset for courses."""

    queryset = Course.objects.all()
    pagination_class = CustomPagination

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
    """Создание урока."""

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
    """Список уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    """Детальный просмотр урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModers | IsOwner,
    )


class LessonUpdateAPIView(UpdateAPIView):
    """Редактирование урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModers | IsOwner,
    )


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsOwner | ~IsModers,
    )


class SubscriptionAPIView(APIView):
    """Контроллер для управления подпиской"""

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="""
           Управление подпиской.
           Если пользователь уже подписан - подписка удаляется.
           Если не подписан - подписка добавляется.
           """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["course_id"],
            properties={
                "course_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="id курса", example=1
                ),
            },
            example={"course_id": 1},
        ),
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=["подписка удалена", "подписка добавлена"],
                        ),
                    },
                ),
                examples={
                    "application/json": {
                        "examples": {
                            "удаление": {"message": "подписка удалена"},
                            "создание": {"message": "подписка добавлена"},
                        }
                    }
                },
            )
        },
    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"

        else:
            subs_item = Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message})
