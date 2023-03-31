from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', views.CustomSimpleJWTLoginView.as_view(), name='login_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.CreateUserView.as_view(), name='sign_up_view'),
    path('get_billing_key/', views.GetBillingKeyView.as_view(), name='get_billing_key_view')
]
