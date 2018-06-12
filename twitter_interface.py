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
LOG = os.environ['LOG'] == 'True'

HASHTAG_FIND = '#100diasdecodigo'
HASHTAG_ENGAGE = '#100diasdecodigo #100daysofcoding #DevsOnBeer'
DATE_TODAY = datetime.today().strftime('%Y-%m-%d')
ID_MYSELF = 1003663176280559617

def to_dict(abstract_object):
    return json.loads(str(abstract_object))

def get_tweets(hashtag, day, api):
    tweets_related =  api.GetSearch(term=hashtag, since=day)
    # Convert to dictionary, 'cause reasons
    tweets_dict = [to_dict(t) for t in tweets_related]
    return tweets_dict

def follow_back(tweets, api):
    ids_follow_back = set([t['user']['id'] for t in tweets])
    for user_id in ids_follow_back:
        if user_id != ID_MYSELF:
            log = api.CreateFriendship(user_id=user_id)
            yield to_dict(log)

# Retweet filter
def filter_retweet(tweets):
    return [t for t in tweets if not 'retweeted_status' in t.keys()]

# Maybe useless
def filter_exception_list(tweets):
    exception_list = [
        1003579193907654657, # cemdiasdecodigo
        1003848514823213056, # _30days30sites
        ID_MYSELF,
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

def run_daily(api):
    tw_raw = get_tweets(HASHTAG_FIND, DATE_TODAY, api)
    tw_filtered = filter_tweets(tw_raw)

    if FOLLOW:
        for log_follow in follow_back(tw_raw, api):
            print("Follow Back: {}".format(log_follow['screen_name']))
    
    if LOG or True:
        for t in tw_filtered:
            print("Count: {1} - \'{0}\'".format(t['user']['screen_name'], \
                t['created_at']))
    return tw_filtered, tw_raw

def post_daily(api, tweets, hashtag=HASHTAG_ENGAGE):
    message = 'Relatório do desafio de 100 dias de Código! Hoje, {} usuários' +\
    ' se engajaram com o desafio {}'
    status = api.PostUpdate(message.format(len(tweets), hashtag))
    return status

def warn_users(api, tweets, days):
    users = ['@'+t['screen_name'] for t in tweets]
    t = ' '.join(users)
    if len(users) == 1:
        msg = 'Hey, {}, você está à {} sem postar! {}'.format(t, days, HASHTAG_ENGAGE)
    else:
        msg = 'Hey, {}, vocês estão à {} sem postar! {}'.format(t, days, HASHTAG_ENGAGE)
    status = api.PostUpdate(msg)
    return status 