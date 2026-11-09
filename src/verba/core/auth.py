import hashlib
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from verba.apps.users.models import RefreshToken

User = get_user_model()

ACCESS_MAX_AGE = settings.JWT_ACCESS_LIFETIME_MINUTES * 60
REFRESH_MAX_AGE = settings.JWT_REFRESH_LIFETIME_DAYS * 24 * 60 * 60


# ---------- Access token ----------


def get_payload_from_request(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return None  # cokkie not exist

    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:  # expireed token also raise this error
        return None  # false or expired token


def create_access_token(user):
    now = datetime.now(UTC)
    payload = {
        "sub": str(user.pk),
        "iat": now,
        "exp": now + timedelta(seconds=ACCESS_MAX_AGE),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


# ---------- Refresh token ----------
def _hash(raw):
    return hashlib.sha256(raw.encode()).hexdigest()


def issue_refresh_token(user):
    raw = secrets.token_urlsafe(48)
    RefreshToken.objects.create(
        user=user,
        token_hash=_hash(raw),
        expires_at=timezone.now() + timedelta(seconds=REFRESH_MAX_AGE),
    )
    return raw  # فقط همین‌جا خام است؛ در دیتابیس فقط هش ذخیره می‌شود


def rotate_refresh_token(raw):
    """refresh معتبر را باطل می‌کند و (user, refresh_جدید) برمی‌گرداند. وگرنه None."""
    record = (
        RefreshToken.objects.select_related("user")
        .filter(token_hash=_hash(raw))
        .first()
    )
    if record is None or record.revoked_at is not None:
        return None
    if record.expires_at <= timezone.now():
        return None

    record.revoked_at = timezone.now()
    record.save(update_fields=["revoked_at"])
    return record.user, issue_refresh_token(record.user)


def revoke_refresh_token(raw):
    RefreshToken.objects.filter(token_hash=_hash(raw), revoked_at__isnull=True).update(
        revoked_at=timezone.now()
    )


# ---------- کوکی‌ها ----------
def set_auth_cookies(response, access, refresh):
    secure = not settings.DEBUG
    response.set_cookie(
        "access_token",
        access,
        httponly=True,
        secure=secure,
        samesite="Lax",
        max_age=ACCESS_MAX_AGE,
    )
    response.set_cookie(
        "refresh_token",
        refresh,
        httponly=True,
        secure=secure,
        samesite="Lax",
        max_age=REFRESH_MAX_AGE,
    )
    # برای JavaScript (دکمه‌ی Log In/Out)؛ باید به اندازه‌ی refresh عمر کند
    response.set_cookie(
        "logged_in",
        "true",
        secure=secure,
        samesite="Lax",
        path="/",
        max_age=REFRESH_MAX_AGE,
    )
    return response


def clear_auth_cookies(response):
    for name in ("access_token", "refresh_token", "logged_in"):
        response.delete_cookie(name)
    return response


def start_session(response, user):
    """بعد از login/register صدا بزنید."""
    return set_auth_cookies(
        response, create_access_token(user), issue_refresh_token(user)
    )


# ---------- احراز هویت یک درخواست ----------
def authenticate(request):
    """
    (user, new_tokens) برمی‌گرداند.
    new_tokens = (access, refresh) فقط وقتی که خودکار refresh شده باشد.
    کاربر نامعتبر: (None, None)
    """
    payload = get_payload_from_request(request)  # تابع فعلی خودتان
    if payload is not None:
        try:
            return User.objects.get(pk=payload["sub"]), None
        except (User.DoesNotExist, KeyError, ValueError):
            pass

    raw = request.COOKIES.get("refresh_token")
    if raw:
        result = rotate_refresh_token(raw)
        if result is not None:
            user, new_refresh = result
            return user, (create_access_token(user), new_refresh)

    return None, None
