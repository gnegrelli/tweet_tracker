import re
from typing import List

from django.db import models
from django.utils.functional import cached_property

from .stopwords import stopwords
from .tokenizer import CustomTokenizer


RE_TWEET_PATTERN = r'^[@a-záàâãéèêíïóôõöúçñ\d].+'


class TwitterUser(models.Model):
    """Information of Twitter user"""
    twitter_id = models.CharField(max_length=20)
    username = models.CharField(max_length=120)
    profile_name = models.CharField(max_length=120, null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    joined_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile_name} (@{self.username})'

    @property
    def tweets_stored(self) -> int:
        return self.tweets.count()


class Tweet(models.Model):
    """Tweets retrieved from Twitter API"""
    tweet_id = models.CharField(max_length=40)
    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, related_name='tweets')
    content = models.CharField(max_length=400)
    tweeted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    likes = models.IntegerField(null=True, blank=True)
    retweets = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        max_len = 40
        ending = '...' if len(self.content) > max_len else ''
        return f'{self.user!s}: \"{self.content[:max_len]}{ending}\"'

    @cached_property
    def tokens(self) -> List[str]:
        tokenizer = CustomTokenizer(preserve_case=False)
        tokens = tokenizer.tokenize(self.content)

        clean_tokens = [
            token.strip() for token in tokens
            if token.strip() not in stopwords and token.strip() and re.match(RE_TWEET_PATTERN, token)
        ]

        return clean_tokens
