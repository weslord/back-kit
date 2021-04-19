from django.conf import settings

import logging


log = logging.getLogger(__name__)


def send_reset_password_email(user, reset_token):
    reset_url = settings.RESET_PASSWORD_URL.format(
        reset_token=reset_token,
        user_id=user.id
    )
    log.debug('EMAIL: ResetPassword') #, str(user), reset_url)


def send_welcome_email(user):
    log.debug('EMAIL: WelcomeUser', user)
