from django.urls import path
from knox import views as knox_views

from authentication.views import (
    AdditionalDetailsAPIView,
    LoginAPIView,
    OAuthAPIView,
    RegisterAPIView,
    ResetPasswordVerificationAPIView,
    VerificationAPIView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    path("verify/", VerificationAPIView.as_view(), name="verify"),
    path(
        "verify/reset-pass/",
        ResetPasswordVerificationAPIView.as_view(),
        name="verify-password",
    ),
    path("oauth/", OAuthAPIView.as_view(), name="oauth"),
    path("profile/", AdditionalDetailsAPIView.as_view(), name="profile"),
]
