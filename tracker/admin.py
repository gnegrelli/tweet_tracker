from django.contrib import admin

from .forms import TweetForm
from .models import Tweet, TwitterUser


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        'tweet_id',
        '__str__',
        'tweeted_at',
        'likes',
        'retweets',
        'deleted'
    )
    list_filter = ('user', 'deleted',)
    search_fields = ('tweet_id',)
    form = TweetForm


@admin.register(TwitterUser)
class TwitterUserAdmin(admin.ModelAdmin):
    list_display = (
        'twitter_id',
        '__str__',
        'followers',
        'verified',
        'joined_at'
    )
