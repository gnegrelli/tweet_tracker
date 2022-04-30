import sys

from django.apps import AppConfig
from django.conf import settings


class TrackerConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    def ready(self):
        """Add/Update users every time backend starts"""
        if 'migrate' in sys.argv:
            return

        from .services import add_twitter_users
        if not settings.DEBUG:
            print('Adding users...')
            # add_twitter_users(settings.USERS)
