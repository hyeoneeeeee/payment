from django.urls import path
from payment import views


urlpatterns = [
    path("charging_point/", views.PointChangingView.as_view(), name="changing_point_view"),
    path("create_coupon/", views.CreateCouponView.as_view(), name="create_coupon_view"),
    path("using_coupon/", views.UsingCouponView.as_view(), name="using_coupon_view"),
]