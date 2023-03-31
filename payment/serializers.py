from rest_framework import serializers
from payment.models import CouponList, Payment, UsedCouponList


class CreateCouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = CouponList
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields ="__all__"


class UsedCouponListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsedCouponList
        fields = "__all__"

