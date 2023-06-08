from django.urls import path, include
from Account.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    
    # Access Token Create ( আমাদের user authenticate হাঁ কি না , এইটি নির্দেশ করে )
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Refresh Token Create ( Access Token expire হয়ে গেলে নতুন করে Access Token generate করে দেয় )  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Verify The Token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     

    path('register/', UserRegistrationView.as_view(), name='UserRegistrationView'),
    path('login/', UserLoginView.as_view(), name='UserLoginView'),
    path('profile/', UserProfileView.as_view(), name='UserProfileView'),
    path('change-password/', UserChangePasswordView.as_view(), name='UserChangePasswordView'),
    path('reset-password-email-send/', SendPasswordResetEmailView.as_view(), name='SendPasswordResetEmailView'),

    # IF Link Verification
    # path('reset-password-email-verify/<uid>/<token>/', UserPasswordResetView.as_view(), name='UserPasswordResetSerializer'),

    # IF OTP Virefication
    path('reset-password-email-verify/', UserPasswordResetView.as_view(), name='UserPasswordResetSerializer'),





    # For Session Authentication Weneed Login Form, That whay it are needed.
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]





## Surver = http://127.0.0.1:8000/api/token/

"""
{
  "username": "admin",
  "password": "admin"
  
}

When Access Token Time Out = {"refresh":"Your Refesh Token"}

"""