import re

import nltk

def clean(tweets):
    """
    Utility method, cleans up the raw text of the user's tweets, tokenizes
    them, and returns them as a single document.
    """
    # We have a whole list of tweets. We don't really care about all the
    # associated metadata (that's for another round of analytics!), so we're
    # only going to process the "text" field of the tweet objects.
    tokens = []
    for tweet in tweets:
        tokens.extend(_tokenize(tweet['text']))

    # Rules:
    # - No URLs, stop words, @-replies.
    # Hashtags are cool.
    tokens = filter(_minlength, tokens)
    tokens = filter(_urls, tokens)
    tokens = filter(_stopwords, tokens)
    tokens = filter(_replies, tokens)

    # K, that's it.
    return tokens

def _tokenize(text):
    return nltk.tokenize.casual_tokenize(text)

def _minlength(s):
    return len(s) > 2

def _urls(s):
    """
    Yoinked viciously from:
    https://github.com/alexperrier/datatalks/blob/master/twitter/twitter_tokenize.py#L81
    """
    return re.match(r"(?:\@|http?\://)\S+", s) is None and \
        re.match(r"(?:\@|https?\://)\S+", s) is None

def _stopwords(s):
    return s not in nltk.corpus.stopwords.words("english")

def _replies(s):
    return s[0] != '@'
