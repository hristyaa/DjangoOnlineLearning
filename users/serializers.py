from rest_framework.serializers import ModelSerializer

from users.models import Payment, User
from users.validators import validate_paid_course_or_lesson


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["user", "date_paid", "payment_amount"]

    def validate(self, data):
        validate_paid_course_or_lesson(data.get("paid_course"), data.get("paid_lesson"))
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
