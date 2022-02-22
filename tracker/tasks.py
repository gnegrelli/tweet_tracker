from celery import shared_task

from .models import Tweet, TwitterUser
from .services import get_user_tweets_paginated


@shared_task(name='fetch_new_tweets')
def fetch_new_tweets():
    for twitter_user in TwitterUser.objects.all().distinct():
        last_tweet_id = Tweet.objects.filter(user=twitter_user).order_by('-tweet_id').first().tweet_id
        print(f'Fetching tweets from {twitter_user.username} since tweet id {last_tweet_id}...')
        get_user_tweets_paginated(twitter_user, params={'since_id': last_tweet_id})
