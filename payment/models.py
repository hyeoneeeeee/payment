from django.db import models
from usage.models import Usage
from user.models import UserModel
# Create your models here.

class Payment(models.Model):
    buyer_name = models.ForeignKey(UserModel, verbose_name="결제한 유저", on_delete=models.DO_NOTHING)
    usage_id = models.ForeignKey(Usage, verbose_name="사용 번호", on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(verbose_name="결제 목적", max_length=50)
    amount = models.IntegerField(verbose_name="결제 금액")
    payment_time = models.TextField(verbose_name="결제 시간")
    usage_time = models.TextField(verbose_name="사용 시간", blank=True)
    imp_uid = models.TextField(verbose_name='결제번호', blank=True)
    merchant_uid = models.TextField(verbose_name='주문번호', blank=True)

class CouponList(models.Model):
    coupon_name = models.CharField(verbose_name='쿠폰 이름', max_length=50)
    coupon_num = models.TextField(verbose_name="쿠폰번호")
    available = models.BooleanField(default=True, verbose_name="사용가능여부") #True=사용가능 쿠폰, False=사용불가능 쿠폰
    charging_point = models.IntegerField(verbose_name="적립금액")

    def __str__(self):
        return self.coupon_name


class UsedCouponList(models.Model):
    user_id= models.ForeignKey(UserModel, verbose_name="쿠폰사용유저", on_delete=models.DO_NOTHING, related_name="get_user_id")
    coupon_name = models.ForeignKey(CouponList, verbose_name="쿠폰 이름", on_delete=models.DO_NOTHING, related_name="get_coupon_name")
    using_coupon_time = models.DateTimeField(verbose_name='쿠폰사용 시간' ,auto_now_add=True)
