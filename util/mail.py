from django.conf import settings

import json
import logging
import requests


log = logging.getLogger(__name__)


def send_mail(email, subject, text_body):
    url = "https://api.postmarkapp.com/email"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": settings.POSTMARK_API_KEY,
    }

    data = {
        "From": settings.POSTMARK_SENDER_EMAIL,
        "To": email,
        "Subject": subject,
        "TextBody": text_body,
        "MessageStream": "outbound",
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.ok:
        log.debug(f"Mail sent to {email}: {subject}")
    else:
        log.warning(f"Mail delivery error {response.status_code}: {response.json()}")

    return response


def send_templated_mail(email, template_alias, template_data):
    url = "https://api.postmarkapp.com/email/withTemplate"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": settings.POSTMARK_API_KEY,
    }

    data = {
        "From": settings.POSTMARK_SENDER_EMAIL,
        "To": email,
        "TemplateAlias": template_alias,
        "TemplateModel": template_data,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.ok:
        log.debug(f"Mail sent to {email}: {template_alias}")
    else:
        log.warning(f"Mail delivery error {response.status_code}: {response.json()}")

    return response
