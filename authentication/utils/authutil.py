import os
import threading
from datetime import datetime, timedelta

from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class AuthenticationUtil:
    def encrypt(self, data):
        """Returns signed email using Django Secret Key."""

        signer = signing.Signer(salt=settings.SECRET_KEY)
        # data["timestamp"] = int(datetime.now().timestamp())
        enc = signer.sign_object(data)  # also supports other types
        return enc

    def decrypt(self, enc):
        """Returns decrypted email and error if any."""

        signer = signing.Signer(salt=settings.SECRET_KEY)
        try:
            data = signer.unsign_object(enc)
            return data
        except signing.BadSignature as e:
            print(e)
            return None

    # def is_enc_expired(self, enc):
    #     """Returns boolean value if the enc expired or not"""

    #     data = self.decrypt(enc)
    #     enc_datetime = datetime.fromtimestamp(data["timestamp"])

    #     if datetime.now() - enc_datetime > timedelta(hours=2):
    #         return True

    #     return False

    def send_verification_email_thread(self, user, new_data):
        data = {"email": user.email, **new_data}
        enc = self.encrypt(data)
        url = os.getenv("FRONTEND_URL") + "api/auth/verify/" + enc
        if new_data:
            url = os.getenv("FRONTEND_URL") + "api/auth/reset-pass/" + enc
        context = {"link": url, "first_name": user.first_name}
        html_message = render_to_string("emailverify.html", context=context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Pecfest Verification",
            message=plain_message,
            from_email=f"Pecfest <{settings.EMAIL_HOST_USER}>",
            recipient_list=[user.email],
            html_message=html_message,
        )

    def send_verification_email(self, user, new_data={}):
        t = threading.Thread(
            target=self.send_verification_email_thread, args=(user, new_data)
        )
        t.start()
