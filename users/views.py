from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentListAPIView(ListAPIView):
    """Вывод списка платежей с возможностью фильтрации по курсу, уроку и способу оплаты, сортировке по дате оплаты"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("date_payed",)
