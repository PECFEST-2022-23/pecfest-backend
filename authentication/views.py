# from django.contrib.auth.tokens import default_token_generator
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.constants import UserAuthStatus
from authentication.models import User, UserDetails
from authentication.serializers import (
    OAuthSerializer,
    RegisterSerializer,
    UserDetailsSerializer,
    UserSerializer,
)
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

    def patch(self, request, *args, **kwargs):
        data = request.data
        email = data.get("email")
        new_pass = data.get("password")
        res = {"user_status": UserAuthStatus.message}
        if not email and not new_pass:
            res["message"] = "Invalid Data"
            return Response(
                res,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            res["message"] = "Email Id doesn't exist"
            return Response(
                res,
                status=status.HTTP_400_BAD_REQUEST,
            )

        AuthenticationUtil().send_verification_email(user, {"new_password": new_pass})
        res["message"] = "Please Verify the link sent on your email"
        return Response(res, status=status.HTTP_200_OK)


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
        data["user"] = UserSerializer(user).data

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class VerificationAPIView(GenericAPIView, AuthenticationUtil):
    permission_classes = (AllowAny,)

    # to verify email
    def post(self, request, *args, **kwargs):
        enc = request.data.get("token")

        data = self.decrypt(enc)
        user = User.objects.get(email=data["email"])
        user.is_active = True
        user.save()

        return Response(
            {"message": "Account Sucessfully Verified"},
            status=status.HTTP_200_OK,
        )

    # to resend email
    def patch(self, request, *args, **kwargs):
        enc = request.data.get("token")
        data = self.decrypt(enc)
        user = User.objects.get(email=data["email"])

        self.send_verification_email(user)

        return Response(
            {"message": "Verification link sent successfully"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordVerificationAPIView(GenericAPIView, AuthenticationUtil):
    permission_classes = (AllowAny,)

    # to update password email
    def post(self, request, *args, **kwargs):
        enc = request.data.get("token")

        data = self.decrypt(enc)
        user = User.objects.get(email=data["email"])
        user.set_password(data["new_password"])
        user.save()

        return Response(
            {"message": "Password Verified Successfully"},
            status=status.HTTP_200_OK,
        )


class OAuthAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get("email")
        data = {}
        if not serializer.is_valid():
            data["user_status"] = UserAuthStatus.message
            data["message"] = "Invalid Data"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = serializer.save()

        if not UserDetails.objects.filter(user=user).exists():
            data["user_status"] = UserAuthStatus.verified
        else:
            data["user_status"] = UserAuthStatus.completed

        data["token"] = AuthToken.objects.create(user)[1]
        data["user"] = UserSerializer(user).data

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class AdditionalDetailsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailsSerializer
    queryset = UserDetails.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            obj = UserDetails.objects.get(user=request.user)
        except UserDetails.DoesNotExist:
            return Response(
                {"message": "Additional Details doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        data["user"] = str(request.user.id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Additional Details added"}, status=status.HTTP_201_CREATED
        )

    def patch(self, request, *args, **kwargs):
        data = request.data
        try:
            obj = UserDetails.objects.get(user=request.user)
        except UserDetails.DoesNotExist:
            return Response(
                {"message": "Additional Details doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Additional Details updated"}, status=status.HTTP_201_CREATED
        )
