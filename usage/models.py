from django.db import models
from user.models import UserModel


class Usage(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="사용유저", on_delete=models.DO_NOTHING)
    start_time =models.DateTimeField(verbose_name="사용시작 시간", auto_now_add=True,)
    end_time = models.DateTimeField(verbose_name="사용종료 시간", blank=True, null=True)
    usage_time = models.TextField(verbose_name="사용한 시간", blank=True, null=True)
