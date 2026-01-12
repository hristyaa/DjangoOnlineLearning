from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (create_srtipe_session, create_stripe_price,
                            create_stripe_product)


class PaymentListAPIView(ListAPIView):
    """Вывод списка платежей с возможностью фильтрации по курсу, уроку и способу оплаты, сортировке по дате оплаты"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("date_payed",)


class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Для просмотра списка пользователей"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    """Для просмотра одного пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """Для редактирования пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    """Для удаления пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentCreateAPIView(CreateAPIView):
    """Создание платежа"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.paid_course:
            product_name = payment.paid_course.name
            product_description = payment.paid_course.description
            payment_amount = payment.paid_course.amount
        elif payment.paid_lesson:
            product_name = payment.paid_lesson.name
            product_description = payment.paid_lesson.description
            payment_amount = payment.paid_lesson.amount
        product = create_stripe_product(product_name, product_description)
        price = create_stripe_price(product.id, payment_amount)
        session_id, payment_link = create_srtipe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.payment_amount = payment_amount
        payment.save()
