import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserSession


@receiver(post_save, sender = UserSession)
def sig_user_logged_in(sender, user, request, **kwargs):
    print('='*100)
    print("haha")
    print('='*100)
    logger = logging.getLogger(__name__)
    logger.debug("user logged in: %s at %s" % (user, request.META['REMOTE_ADDR']))
