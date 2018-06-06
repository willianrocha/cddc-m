import os
import twitter
from datetime import datetime
import json
from collections import Counter

c_key = os.environ['CONSUMER_KEY']
c_secret = os.environ['CONSUMER_SECRET']
a_token = os.environ['ACCESS_TOKEN']
a_secret = os.environ['ACCESS_SECRET']
FOLLOW = os.environ['FOLLOW'] == 'True'
FOLLOW = os.environ['LOG'] == 'True'

HASHTAG_FIND = '#100diasdecodigo'
HASHTAG_ENGAGE = '#100diasdecodigo #100daysofcoding #DevsOnBeer'
DATE_TODAY = datetime.today().strftime('%Y-%m-%d')

def get_tweets(hashtag, day, api):
    tweets_related =  api.GetSearch(term=hashtag, since=day)
    # Convert to dictionary, 'cause reasons
    tweets_dict = [json.loads(str(t)) for t in tweets_related]
    return tweets_dict

def follow_back(tweets, api):
    ids_follow_back = set([t['user']['id'] for t in tweets])
    for user_id in ids_follow_back:
        log = api.CreateFriendship(user_id=user_id)
        yield log

# Retweet filter
def filter_retweet(tweets):
    return [t for t in tweets if not 'retweeted_status' in t.keys()]

# Maybe useless
def filter_exception_list(tweets):
    exception_list = [
        1003579193907654657, # cemdiasdecodigo
        1003848514823213056, # _30days30sites
    ]
    return [t for t in tweets if not t['user']['id'] in exception_list]

def filter_tweets(tweets):
    valid_tweets = filter_retweet(tweets)
    valid_tweets = filter_exception_list(valid_tweets)
    return valid_tweets

def connect():
    api = twitter.Api(  consumer_key=c_key,
                        consumer_secret=c_secret,
                        access_token_key=a_token,
                        access_token_secret=a_secret)
    return api

def run(api):
    tw = get_tweets(HASHTAG_FIND, DATE_TODAY, api)
    tw = filter_tweets(tw)

    if FOLLOW:
        for log_follow in follow_back(tw, api):
            if LOG: print(log_follow)

    message = 'Relatório do desafio de 100 dias de Código! Hoje, {} usuários' +\
    ' se engajaram com o desafio {}'
    status = api.PostUpdate(message.format(len(tw), HASHTAG_ENGAGE))
    return status
