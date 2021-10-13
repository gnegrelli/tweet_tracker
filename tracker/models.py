from django.db import models


class TwitterUser(models.Model):
    """Information from Twitter user"""
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


class Tweet(models.Model):
    """Tweets retrieved from Twitter API"""
    tweet_id = models.CharField(max_length=40)
    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, related_name='tweets')
    content = models.CharField(max_length=400)
    relevant_tokens = models.CharField(max_length=400)
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
