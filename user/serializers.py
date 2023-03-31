from rest_framework import serializers
from user.models import UserModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.user_id
        token['is_admin'] = user.is_admin
        return token


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = super().create(validated_data)
        user_id = user.user_id
        user_password = user.password
        user.set_password(user_password)
        user.save()
        return user

    class Meta:
        model = UserModel
        fields = "__all__"
