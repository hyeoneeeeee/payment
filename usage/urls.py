from django.urls import path
from usage import views


urlpatterns = [
    path("start_charging/", views.StartChargingView.as_view(), name="start_charging_view"), #충전 시작
    path("stop_charging/", views.StopChargingView.as_view(), name="stop_charging_view"), #충전 종료
]