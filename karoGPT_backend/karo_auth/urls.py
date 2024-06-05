# karo_auth/urls.py
from django.urls import path

from karo_auth.views import UserCreateAPIView, MyTokenObtainPairView, TokenRefreshView, MyTestView


urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', UserCreateAPIView.as_view(), name='user_create'),
    path('api/test-auth-flow/', MyTestView.as_view(), name='test_auth_flow'),
]
