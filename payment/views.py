from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from user.models import UserModel
from payment.models import CouponList
from rest_framework import status, permissions
from payment.serializers import CreateCouponSerializer, PaymentSerializer, UsedCouponListSerializer
import requests
from payment_model.settings import IMP_KEY, IMP_SECRET


# pg사 access token발급
def get_iamport_access_token():
        payment_token_uri = 'https://api.iamport.kr/users/getToken'
        request_parameter = {
            "imp_key": IMP_KEY,
            "imp_secret": IMP_SECRET,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_json = requests.post(payment_token_uri, headers=token_headers, data=request_parameter).json()
        return token_json['response']['access_token']

#결제취소 요청
def request_payment_cancle(imp_uid, amount, access_token):
        uri = f'https://api.iamport.kr/payments/cancel?_token={access_token}'
        body = {
            "reason": "결제 조작 의심 취소",
            "imp_uid": imp_uid,
            "amount": amount,
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Authorization' : access_token
        }
        response = requests.post(uri,body,headers)
        return response

class PointChangingView(APIView):
    def get(self, request):
        user = get_object_or_404(UserModel, user_id=request.GET.get("user_id",None))
        if user.billing_key != None:
            return Response({"billing_key":user.billing_key})
        else:
            return Response({"billing_key":""})


    def post(self, request):
        user = get_object_or_404(UserModel, user_id=request.data["buyer_name"])
        access_token = get_iamport_access_token()
        amount = int(request.data["amount"])

        #빌링키 있을때
        if "customer_uid" in request.data:
            url = f"https://api.iamport.kr/subscribe/payments/again?_token={access_token}"
            data = request.data
            billing_key_payment_json = requests.post(url=url, data=data).json()
            data["imp_uid"] = billing_key_payment_json["response"]["imp_uid"]
            data["buyer_name"] = user.pk
            billing_key_serializer = PaymentSerializer(data=data)
            if billing_key_serializer.is_valid():
                billing_key_serializer.save()
                setattr(user, "point", user.point + amount)
                user.save()
                return Response({"message":f"등록된 카드로 {amount}원이 결제되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"message":billing_key_serializer.errors})

        # 빌링키 없을 때
        else:
            imp_uid = request.data["imp_uid"]
            #결제정보 확인 로직
            payment_confirmation_uri = f'https://api.iamport.kr/payments/{imp_uid}?_token={access_token}'
            response_json = requests.post(payment_confirmation_uri).json()
            paied_amount = response_json["response"]["amount"]
            data = request.data
            data["buyer_name"] = user.pk

            #실결제금액과, 입력받은 값이 다를 경우 결제취소
            if paied_amount != amount:
                request_payment_cancle(imp_uid=imp_uid, amount=paied_amount, access_token=access_token)
                return Response({"message":"결제오류"})

            else:
                serializer = PaymentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    setattr(user, "point", user.point + amount)
                    user.save()
                    return Response({"message":"결제 성공"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message":"결제정보가 올바르지 않습니다","error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UsingCouponView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        user = get_object_or_404(UserModel, user_id=request.user)
        coupon = get_object_or_404(CouponList, coupon_num=request.data["coupon_num"])
        if coupon.available == False:
            return Response({"message":"사용 불가능한 쿠폰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data={
                "user_id":request.user.pk,
                "coupon_name":coupon.pk
            }
            serializer = UsedCouponListSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"message":"사용자 정보가 맞지 않습니다.","error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            user_point = getattr(user, "point")
            setattr(user, "point", user_point + coupon.charging_point)
            user.save()
            setattr(coupon, "available", False)
            coupon.save()
            return Response({"message":f"{coupon.charging_point}점이 충전되었습니다"}, status=status.HTTP_200_OK)


class CreateCouponView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def post(self, request):
        if CouponList.objects.filter(coupon_num=request.data["coupon_num"]):
            return Response({"message":"이미 존재하는 쿠폰번호 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        seializer = CreateCouponSerializer(data=request.data)
        if seializer.is_valid():
            seializer.save()
            return Response({"message":"쿠폰등록 완료"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"쿠폰등록 실패","error":seializer.errors}, status=status.HTTP_400_BAD_REQUEST)
