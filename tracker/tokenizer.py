import re

from nltk.tokenize import TweetTokenizer
from typing import List


class CustomTokenizer(TweetTokenizer):

    MEDIA_RE = re.compile(r'https?://t\.co\S*')

    def tokenize(self, text: str) -> List[str]:
        return [token for token in super().tokenize(text) if not self.MEDIA_RE.match(token)]
