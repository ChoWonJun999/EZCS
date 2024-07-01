import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    logger = logging.getLogger(__name__)
    logger.debug("user logged in: %s at %s" % (user, request.META['REMOTE_ADDR']))
