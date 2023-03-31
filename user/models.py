from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, user_id, password):

        if not user_id:
            raise ValueError('User must have an user_id')
        if not password:
            raise ValueError('User must have a password')

        instance = self.model(
            user_id=user_id,

        )
        instance.set_password(password)
        instance.save(using=self._db)
        return instance

    def create_superuser(self, user_id, password=None):

        instance = self.create_user(
            user_id = user_id,
            password=password,
        )
        instance.is_admin = True
        instance.save(using=self._db)
        return instance


class UserModel(AbstractBaseUser):
    user_id = models.CharField(unique=True, verbose_name='아이디', max_length=50, blank=False, null=False)
    password = models.CharField(verbose_name='비밀번호', max_length=30, blank=False, null=False)
    billing_key = models.TextField(verbose_name='빌링 키', blank=True, null=True)
    point = models.IntegerField(verbose_name='포인트', default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

