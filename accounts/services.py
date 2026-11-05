import secrets

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail

from .models import EmailOTP

MAX_ATTEMPTS = 5


def send_otp(user):
    code = f"{secrets.randbelow(1_000_000):06d}"
    EmailOTP.objects.update_or_create(
        user=user,
        defaults={"code_hash": make_password(code), "attempts": 0},
    )
    send_mail(
        subject="Your Project Creator verification code",
        message=f"Your OTP is {code}. It is valid for 1 minute.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def verify_otp(user, code):
    try:
        otp = user.email_otp
    except EmailOTP.DoesNotExist:
        return False, "No OTP found. Please request a new one."

    if otp.is_expired():
        return False, "OTP expired. Please request a new one."
    if otp.attempts >= MAX_ATTEMPTS:
        return False, "Too many attempts. Please request a new OTP."

    if not check_password(code, otp.code_hash):
        otp.attempts += 1
        otp.save(update_fields=["attempts"])
        return False, "Invalid OTP."

    otp.delete()
    user.is_active = True
    user.is_email_verified = True
    user.save(update_fields=["is_active", "is_email_verified"])
    return True, "Email verified. You can now log in."