from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import BasePermission

import logging


log = logging.getLogger(__name__)


class AllowNone(BasePermission):
    """
    Deny all access.
    Used as a default permission to ensure permissions are deliberately set
    on all endpoints.
    """

    def has_permission(self, request, view):
        msg = f'Undefined permissions_classes for {view.__class__}'

        if (settings.DEBUG):
            raise ImproperlyConfigured(msg)
        else:
            log.error(msg)
            return False
