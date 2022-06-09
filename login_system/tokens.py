import base64

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """
    django supports token creation for resetting passwords. Token is safe, because it gets invalid when the
    user changes their's password. For verification we have to overwrite one function and do not use password
    for making hash value

    """
    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{timestamp}{user.is_active}'


def create_url(request, token, uid):
    host = request.META['HTTP_HOST']  # get ,,domain'' of the webapp
    """
    I used base64 because it can use only characters that are allowed to be in URL. We have to encode uid and token 
    so it will be treated as bytes and then decode bytes to string. we need to use separator between uid and token, 
    because later on when we decode we need to know which user to verify
    """

    return f'http://{host}/activate/{base64.b64encode(f"{uid}|{token}".encode("ascii")).decode("ascii")}'


account_activation_token = TokenGenerator()  # creating tokengenerator object
