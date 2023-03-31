from rest_framework import status
from rest_framework.response import Response
from usage.models import Usage
from user.models import UserModel
from payment.models import Payment
from rest_framework.views import APIView
from datetime import datetime
from payment.serializers import PaymentSerializer
from usage.serializers import StartChargingSerializer
from rest_framework.generics import get_object_or_404
import requests
from payment.views import get_iamport_access_token



class StartChargingView(APIView):
    # permission_classes=[permissions.IsAuthenticated]
    def post(self, request):
        user = get_object_or_404(UserModel, user_id=request.GET.get("user_id", None))
        try:
            usage_data = Usage.objects.filter(user=user.pk).order_by("-pk")[0]
            if usage_data and usage_data.end_time==None:
                return Response({"message":"이미 충전중인 내역이 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = StartChargingSerializer(data={"user":user.pk})
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"충전이 시작되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"오류가 발생하였습니다", "error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            serializer = StartChargingSerializer(data={"user":user.pk})
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"충전이 시작되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"오류가 발생하였습니다", "error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class StopChargingView(APIView):
    # permission_classes=[permissions.IsAuthenticated]
    def post(self, request):
        print(request.data["user_id"])
        user = get_object_or_404(UserModel, user_id=request.data["user_id"])
        usage_data = Usage.objects.filter(user=user.pk).order_by("-pk")[0]
        user_point = user.point
        print(1)
        if usage_data.end_time == None:
            now = datetime.now()
            date_to_compare = datetime.strptime('19700101', '%Y%m%d')
            end_time = datetime.now()
            usage_time = end_time - usage_data.start_time
            minutes = usage_time.total_seconds()/60
            amount = f"{minutes*100:.0f}"
            amount = int(amount)
            setattr(usage_data, "end_time", end_time)
            setattr(usage_data, "usage_time", usage_time)
            setattr(usage_data, "payment_amount", amount)
            usage_data.save()
            diff_time = now - date_to_compare
            diff_time = diff_time.microseconds

            #포인트로 결제 가능할 때
            if user_point >= amount:
                data = {
                    "buyer_name": user.pk,
                    "amount": amount,
                    "payment_time": str(now),
                    "merchant_uid": "",
                    "name": "포인트로 결제",
                    "usage_id":usage_data.pk
                }
                payment_serializer = PaymentSerializer(data=data)
                if payment_serializer.is_valid():
                    payment_serializer.save()
                    setattr(user, "point", user_point - amount)
                    user.save()
                    return Response({"message":f"충전이 종료되었습니다. 사용시간은 {usage_time}, 차감 포인트는 {amount} 포인트입니다. {user.point}포인트가 남았습니다."}, status=status.HTTP_200_OK)
                else:
                    return Response({"message":payment_serializer.errors}, status=status.HTTP_404_NOT_FOUND)

            #자동결제 카드가 등록되어 있고, 포인트가 모자랄 때
            elif user_point < amount and user.billing_key != None:
                print(3)
                access_token = get_iamport_access_token()
                data = {
                    "buyer_name": user.user_id,
                    "amount": amount - user_point,
                    "customer_uid" :user.billing_key,
                    "payment_time": str(now),
                    "merchant_uid": "merchant_uid_" + f"{diff_time}",
                    "name": "포인트 차감 후 자동결제"
                }
                url = f"https://api.iamport.kr/subscribe/payments/again?_token={access_token}"
                response_json = requests.post(url=url, data=data).json()
                data["imp_uid"] = response_json["response"]["imp_uid"]
                data["usage_id"] = usage_data.pk
                payment_serializer = payment_serializer = PaymentSerializer(data=data)
                if payment_serializer.is_valid():
                    payment_serializer.save()
                    setattr(user, "point", 0)
                    user.save()
                    return Response({"message":f"충전이 종료되었습니다. 사용시간은 {usage_time}입니다. {user_point}포인트 차감 후, {amount-user_point}원 자동결제 되었습니다."}, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            # 포인트도 없고, 자동결제도 등록되어있지 않을 때
            else:
                print(4)
                data = {
                    "buyer_name": user.user_id,
                    "amount": f"{amount - user_point}",
                    "merchant_uid": f"merchant_uid_{diff_time}",
                    "name": "포인트 차감 후 결제요청"
                }
                setattr(user, "point", 0)
                user.save()
                return Response({"message":"결제필요","data":data})
        else:
            return Response({"message":"이미 처리된 내역입니다."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        payment_data = get_object_or_404(Payment, merchant_uid=request.data["merchant_uid"])
        setattr(payment_data, "imp_uid", request.data["imp_uid"])
        payment_data.save()
        return Response({"message":"결제되었습니다"}, status=status.HTTP_200_OK)


