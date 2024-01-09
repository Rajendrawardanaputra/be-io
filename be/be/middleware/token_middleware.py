# authentication.py
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

def get_raw_token(request):
    # Menerima token dari header Authorization
    authorization_header = request.headers.get('Authorization')

    if authorization_header and authorization_header.startswith('Bearer '):
        return authorization_header.split(' ')[1]

    return None

def validate_token(token):
    try:
        data_token = jwt.decode(token, key=settings.SECRET_KEY, algorithms="HS256")
        return data_token
    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed("Token has expired", code=401) from e
    except jwt.DecodeError as e:
        raise AuthenticationFailed(f"Token is invalid {e}", code=401) from e
    except Exception as e:
        raise AuthenticationFailed(str(e))

class DictToObject:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = get_raw_token(request)
        if token is None:
             raise AuthenticationFailed("Token is invalid")

        try:
            valid_token = validate_token(token)
            return DictToObject(**valid_token), None
        except AuthenticationFailed as e:
            raise e
        except Exception as e:
            raise AuthenticationFailed(str(e), code="authentication_failed")