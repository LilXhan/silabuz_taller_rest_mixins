from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path

urlpatterns = [
    path(r'token', TokenObtainPairView.as_view(), name='token'),
    path(r'token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]