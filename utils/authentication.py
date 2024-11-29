"""
This module contains all the authentication related utilities
"""

from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from django.utils.timezone import now
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from utils.redis import RedisCacheMixin

User = get_user_model()


def create_user_jwt_token(user_id: str, expiry: int = 259200) -> str:
    """
    This function creates a jwt token for a user
    """

    payload = {
        "user_id": str(user_id),
        "iat": now(),
        "exp": now() + timedelta(seconds=expiry),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_user_jwt_token(token: str) -> dict | None:
    """
    This function decodes a jwt token for a user
    """
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidSignatureError,
        jwt.InvalidTokenError,
        jwt.DecodeError,
    ) as _error:
        return None


class JWTAuthentication(BaseAuthentication, RedisCacheMixin):
    """
    Custom JWT authentication for DRF
    Extracts the JWT token from the Authorization header
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            # Extract token from "Bearer <token>"
            token_type, token = auth_header.split()
            if token_type.lower() != "bearer":
                return None

            # Decode token and get payload
            payload = decode_user_jwt_token(token)
            if not payload:
                raise AuthenticationFailed("Invalid token")

            # Get user from payload
            if not (user := self.get_cache(key_name=payload["user_id"], model=User)):
                user = User.objects.get(uuid=payload["user_id"])
                self.set_cache(key_name=payload["user_id"], value=user, model=User)

            if not user.is_active:
                raise AuthenticationFailed("User is inactive")

            return (user, token)

        except (ValueError, User.DoesNotExist) as _error:
            raise AuthenticationFailed("Invalid token")

    def authenticate_header(self, request):
        return "Bearer"


class CustomModelBackend(BaseBackend):
    """
    Custom authentication backend that supports both email and username authentication
    """

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            query = Q(is_active=True)
            if username:
                query |= Q(username__iexact=username)
            if email:
                query |= Q(email__iexact=email)

            user = User.objects.get(query)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
