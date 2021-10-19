from typing import List, Optional

from TwitterAPI import TwitterAPI

from django.conf import settings
from django.db.models import Q

from .models import Tweet, TwitterUser


def connect_twitter_api() -> TwitterAPI:
    """Create connector to Twitter API"""
    return TwitterAPI(
        settings.API_KEY, settings.API_KEY_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET, api_version='2'
    )


def add_twitter_users(profile_names: List[str]) -> None:
    """Add users to table TwitterUser"""
    twitter_api = connect_twitter_api()

    profile_names = ','.join(profile_names)

    response = twitter_api.request('users/by', params={'usernames': profile_names})

    if response.status_code == 200:
        users = []
        existing_users = TwitterUser.objects.values_list('twitter_id', flat=True).distinct()
        for user in response:
            if user['id'] not in existing_users:
                users.append(
                    TwitterUser(twitter_id=user['id'], username=user['username'], profile_name=user['name'])
                )

        TwitterUser.objects.bulk_create(users)


def get_user_tweets(user: TwitterUser, params: Optional[dict] = None) -> None:
    """Fetch tweets from user"""
    # Fetch existing tweets from user
    twitter_api = connect_twitter_api()
    tweets = twitter_api.request(f'users/:{user.twitter_id}/tweets', params=params)

    for tweet in tweets:
        defaults = {
            'content': tweet['text'],
            'user': user,
            'relevant_tokens': tweet['text'],
        }
        Tweet.objects.update_or_create(tweet_id=tweet['id'], defaults=defaults)


def set_deleted_tweets(user: TwitterUser) -> None:
    """Update status of deleted tweets"""
    # Fetch existing tweets from user
    twitter_api = connect_twitter_api()
    tweets = twitter_api.request(f'users/:{user.twitter_id}/tweets')
    valid_tweet_ids = [tweet['id'] for tweet in tweets]

    # Update status of tweet instances that are not on Twitter anymore
    deleted_tweets = Tweet.objects.filter(Q(user=user) & ~Q(tweet_id__in=valid_tweet_ids))
    deleted_tweets.update(deleted=True)
