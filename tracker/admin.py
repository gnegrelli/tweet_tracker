from django.contrib import admin

from tracker.models import Tweet, TwitterUser


admin.site.register(TwitterUser)
admin.site.register(Tweet)
