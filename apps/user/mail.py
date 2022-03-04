from django.conf import settings
from util.mail import send_templated_mail

import logging


log = logging.getLogger(__name__)


def send_reset_password_email(user, reset_token):
    reset_url = settings.RESET_PASSWORD_URL.format(reset_token=reset_token, user_id=user.id)

    send_templated_mail(
        user.email,
        "password-reset",
        {"web_url": settings.WEB_URL, "reset_url": reset_url, "user_email": user.email},
    )


def send_welcome_email(user):
    send_templated_mail(
        user.email, "welcome", {"web_url": settings.WEB_URL, "user_email": user.email}
    )
