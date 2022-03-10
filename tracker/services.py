import matplotlib.pyplot as plt
from collections import Counter
from typing import List, Optional
from wordcloud import WordCloud

from TwitterAPI import TwitterAPI, TwitterResponse

from django.conf import settings
from django.db.models import Q
from rest_framework import status

from .exceptions import UnknownUser
from .models import Tweet, TwitterUser


TWEET_QUERY_SIZE = 100


def connect_twitter_api() -> TwitterAPI:
    """Create connector to Twitter API"""
    return TwitterAPI(
        settings.API_KEY, settings.API_KEY_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET, api_version='2'
    )


def add_twitter_users(profile_names: List[str]) -> None:
    """Add users to TwitterUser table and its existing tweets to Tweet table"""
    twitter_api = connect_twitter_api()

    profile_names = ','.join(profile_names)

    response = twitter_api.request(
        'users/by',
        params={'usernames': profile_names, 'user.fields': 'created_at,verified,public_metrics'}
    )

    if response.status_code == status.HTTP_200_OK:
        for user in response:
            defaults = {
                'username': user['username'],
                'profile_name': user['name'],
                'verified': user['verified'],
                'joined_at': user['created_at'],
                'followers': user['public_metrics']['followers_count'],
            }
            user, _ = TwitterUser.objects.update_or_create(twitter_id=user['id'], defaults=defaults)

            # Store all user tweets
            get_user_tweets_paginated(user)


def get_user_tweets(user: TwitterUser, params: Optional[dict] = None) -> TwitterResponse:
    """Fetch tweets from user and store on database"""
    # Create API connector
    twitter_api = connect_twitter_api()

    # Add tweet.fields for date of creation, likes and retweets into params
    tweet_fields = {'created_at', 'public_metrics'}
    if params is None:
        params = {}
    original_tweet_fields = {
        tweet_field.strip() for tweet_field in params.get('tweet.fields', '').split(',') if tweet_field.strip()
    }
    params['tweet.fields'] = ','.join(original_tweet_fields.union(tweet_fields))

    # Fetch existing tweets from user
    response = twitter_api.request(f'users/:{user.twitter_id}/tweets', params=params)

    if response.status_code == status.HTTP_200_OK:
        for tweet in response:
            defaults = {
                'user': user,
                'content': tweet['text'],
                'tweeted_at': tweet['created_at'],
                'likes': tweet['public_metrics']['like_count'],
                'retweets': tweet['public_metrics']['retweet_count'],
            }
            Tweet.objects.update_or_create(tweet_id=tweet['id'], defaults=defaults)

    return response


def get_user_tweets_paginated(user: TwitterUser, params: Optional[dict] = None) -> None:
    """Fetch tweets from user using pagination token"""
    if params is None:
        params = {}
    params.update({'exclude': 'retweets', 'max_results': TWEET_QUERY_SIZE})
    response = get_user_tweets(user, params)

    while 'next_token' in response.json()['meta'].keys():
        # Get pagination token from response
        params['pagination_token'] = response.json()['meta'].get('next_token')

        # Get next page of tweets
        response = get_user_tweets(user, params)


def set_deleted_tweets(user: TwitterUser) -> None:
    """Update status of deleted tweets"""
    # Create API connector
    twitter_api = connect_twitter_api()

    # Fetch active tweets from user
    active_user_tweets = user.tweets.filter(deleted=False).values_list('tweet_id', flat=True)

    # Divide tweet ids in TWEET_QUERY_SIZE chunks
    tweet_id_chunks = [
        active_user_tweets[i:i + TWEET_QUERY_SIZE] for i in range(0, len(active_user_tweets), TWEET_QUERY_SIZE)
    ]

    deleted_tweets = []
    for chunk in tweet_id_chunks:
        # Fetch tweets in chunk from TwitterAPI
        response = twitter_api.request(f'tweets', params={'ids': ','.join(chunk)})

        # Get id of deleted tweets from response content
        if response.status_code == status.HTTP_200_OK:
            deleted_tweets.extend(
                int(error['resource_id']) for error in response.json().get('errors', [])
            )

    # Set deleted attribute to tru for removed tweets
    Tweet.objects.filter(Q(user=user) & Q(tweet_id__in=deleted_tweets)).update(deleted=True)


def build_user_wordcloud(user: TwitterUser) -> None:
    """Create wordcloud based on tweets from user"""
    user_tweets = Tweet.objects.filter(user=user)
    tokens = []
    for user_tweet in user_tweets:
        tokens.extend(user_tweet.tokens)

    wordcloud = WordCloud(background_color=None, mode='RGBA').generate(' '.join(tokens))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


def user_wordcloud(username: str) -> dict:
    """Crete a dictionary with tokens as keys and count as values"""
    user = TwitterUser.objects.filter(username=username)
    if not user:
        raise UnknownUser

    user_tweets = Tweet.objects.filter(user=user[0])

    tokens = Counter()
    for tweet in user_tweets:
        tokens.update(tweet.tokens)

    return dict(tokens)
