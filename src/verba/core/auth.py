import jwt
from django.conf import settings


def get_payload_from_request(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return None  # cokkie not exist

    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:  # expireed token also raise this error
        return None  # false or expired token
