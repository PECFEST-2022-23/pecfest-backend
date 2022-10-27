# from django.contrib.auth.tokens import default_token_generator
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.constants import UserAuthStatus
from authentication.models import User, UserDetails
from authentication.serializers import RegisterSerializer, UserSerializer
from authentication.utils.authutil import AuthenticationUtil


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get("email")
        data = {"user_status": UserAuthStatus.message}

        if User.objects.filter(email=email).exists():
            data["message"] = "Email Already Registered, Please Login"
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not serializer.is_valid():
            data["message"] = "Incorrect Data"
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        data["message"] = "Please Verify the link sent on your email"
        return Response(data, status=status.HTTP_200_OK)


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        data = {}
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            data["user_status"] = UserAuthStatus.message
            data["message"] = "Email Not Registered, Please Register"
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(password):
            data["user_status"] = UserAuthStatus.message
            data["message"] = "Incorrect Password"
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_active:
            data["user_status"] = UserAuthStatus.message
            data["message"] = "Please Verify the link sent on your email"
            AuthenticationUtil().send_verification_email(user)
            return Response(
                data,
                status=status.HTTP_200_OK,
            )

        if not UserDetails.objects.filter(user=user).exists():
            data["user_status"] = UserAuthStatus.verified
        else:
            data["user_status"] = UserAuthStatus.completed

        data["token"] = AuthToken.objects.create(user)[1]

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class VerificationAPIView(GenericAPIView, AuthenticationUtil):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        enc = request.data.get("token")
        if not enc and self.is_enc_expired(enc):
            return Response(
                {"message": "Verification Link Expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = self.decrypt(enc)
        user = User.objects.get(email=data["email"])
        user.is_active = True
        user.save()

        return Response(
            {"message": "Account Sucessfully Verified"},
            status=status.HTTP_204_NO_CONTENT,
        )
