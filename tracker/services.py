from collections import Counter
from typing import List, Optional

from TwitterAPI import TwitterAPI, TwitterResponse

from django.conf import settings
from django.db.models import Q

from .exceptions import UnknownUser
from .models import Tweet, TwitterUser


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

    if response.status_code == 200:
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
            get_all_user_tweets(user)


def get_user_tweets(user: TwitterUser, params: Optional[dict] = None) -> TwitterResponse:
    """Fetch tweets from user"""
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

    if response.status_code == 200:
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


def get_all_user_tweets(user: TwitterUser, params: Optional[dict] = None) -> None:
    """Fetch all previous tweets from user (at least the ones available)"""
    if params is None:
        params = {}
    params.update({'exclude': 'retweets'})
    response = None

    while True:
        # Get id of oldest tweet stored in database
        last_tweet_id = list(response)[-1]['id'] if response is not None else None
        params['until_id'] = last_tweet_id

        # Get tweets older than oldest_tweet
        response = get_user_tweets(user, params)

        # Break if no additional tweet is retrieved
        if response.status_code != 200 or not list(response):
            break


def set_deleted_tweets(user: TwitterUser) -> None:
    """Update status of deleted tweets"""
    # Fetch existing tweets from user
    twitter_api = connect_twitter_api()
    tweets = twitter_api.request(f'users/:{user.twitter_id}/tweets')
    valid_tweet_ids = [tweet['id'] for tweet in tweets]

    # Update status of tweet instances that are not on Twitter anymore
    deleted_tweets = Tweet.objects.filter(Q(user=user) & ~Q(tweet_id__in=valid_tweet_ids))
    deleted_tweets.update(deleted=True)


def build_user_wordcloud(user: TwitterUser) -> None:
    """Create wordcloud based on tweets from user"""
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    user_tweets = Tweet.objects.filter(user=user)
    tokens = []
    for user_tweet in user_tweets:
        tokens.extend(user_tweet.tokens)

    wordcloud = WordCloud(background_color=None, mode='RGBA').generate(' '.join(tokens))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


def user_wordcloud(username: str) -> dict:
    user = TwitterUser.objects.filter(username=username)
    if not user:
        raise UnknownUser
    user_tweets = Tweet.objects.filter(user=user[0])
    tokens = Counter()
    for tweet in user_tweets:
        tokens.update(tweet.tokens)

    return dict(tokens)
