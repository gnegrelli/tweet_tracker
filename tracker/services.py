from typing import List

from TwitterAPI import TwitterAPI

from django.conf import settings

from .models import TwitterUser


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
