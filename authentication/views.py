# from django.contrib.auth.tokens import default_token_generator
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.constants import UserAuthStatus
from authentication.models import User, UserDetails
from authentication.serializers import RegisterSerializer, UserSerializer


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get("email")
        if User.objects.filter(email=email).exists():
            return Response(
                {"user_status": UserAuthStatus.redirect},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not serializer.is_valid():
            return Response(
                {"user_status": UserAuthStatus.incorrect_data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        return Response(
            {"user_status": UserAuthStatus.unverified}, status=status.HTTP_201_CREATED
        )


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        data = {}
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            data["user_status"] = UserAuthStatus.redirect
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(password):
            data["user_status"] = UserAuthStatus.incorrect_data
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_active:
            data["user_status"] = UserAuthStatus.unverified
            #
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


class VerificationAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user

        return Response({}, status=status.HTTP_204_NO_CONTENT)


# from verify_email.token_manager import TokenManager
# verification_url = self.token_manager.generate_link(request, inactive_user, useremail)
# msg = render_to_string(
#                 self.settings.get('html_message_template', raise_exception=True),
#                 {"link": verification_url, "inactive_user": inactive_user},
#                 request=request
#             )
# self.__send_email(msg, useremail)
# subject = self.settings.get('subject')
#         send_mail(
#             subject, strip_tags(msg),
#             from_email=self.settings.get('from_alias'),
#             recipient_list=[useremail], html_message=msg
#         )

# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
