from django.contrib import admin

from tracker.models import Tweet, TwitterUser


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


@admin.register(TwitterUser)
class TwitterUserAdmin(admin.ModelAdmin):
    list_display = (
        'twitter_id',
        '__str__',
        'followers',
        'verified',
        'joined_at'
    )
