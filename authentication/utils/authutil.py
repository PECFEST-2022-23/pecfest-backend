from django.conf import settings
from django.core import signing


class AuthenticationUtil:
    def encrypt(self, dataStr: str):
        """Returns signed email using Django Secret Key."""

        signer = signing.Signer(salt=settings.SECRET_KEY)
        enc = signer.sign_object(dataStr)  # also supports other types
        return enc

    def decrypt(self, enc: str):
        """Returns decrypted email and error if any."""

        signer = signing.Signer(salt=settings.SECRET_KEY)
        try:
            dataStr = signer.unsign_object(enc)
            return dataStr
        except signing.BadSignature as e:
            print(e)
            return None
