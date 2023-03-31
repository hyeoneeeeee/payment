from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import CreateUserSerializer, MyTokenObtainPairSerializer
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from user.models import UserModel
from rest_framework_simplejwt.views import TokenObtainPairView



class CustomSimpleJWTLoginView(TokenObtainPairView):
    serializer = MyTokenObtainPairSerializer


class CreateUserView(APIView):
    def post(self, request):
        user_data = CreateUserSerializer(data=request.data)
        if user_data.is_valid():
            user_data.save()
            return Response({"message": "회원가입에 성공하였습니다"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "회원가입에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)


#빌링키 저장
class GetBillingKeyView(APIView):
    def post(self, request):
        user = get_object_or_404(UserModel, user_id=request.data["user_id"])
        setattr(user, "billing_key", request.data["billing_key"])
        user.save()
        return Response({"message":"카드등록이 완료되었습니다."}, status=status.HTTP_200_OK)
