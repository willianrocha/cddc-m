import os
import twitter
from datetime import datetime
import json
from collections import Counter

c_key = os.environ['CONSUMER_KEY']
c_secret = os.environ['CONSUMER_SECRET']
a_token = os.environ['ACCESS_TOKEN']
a_secret = os.environ['ACCESS_SECRET']

api = twitter.Api(  consumer_key=c_key,
                    consumer_secret=c_secret,
                    access_token_key=a_token,
                    access_token_secret=a_secret)

HASHTAG_FIND = '#100diasdecodigo'
DATE_TODAY = datetime.today().strftime('%Y-%m-%d')

tweets_related =  api.GetSearch(term=HASHTAG_FIND, since=DATE_TODAY)

# follow back
ids_follow_back = set([t.user.id for t in tweets_related])
for user_id in ids_follow_back:
    log = api.CreateFriendship(user_id=user_id)

## Retweet filter
# Retweets can be distinguished from typical Tweets by the existence of a 
# retweeted_status attribute. 
def filter_retweet(list_tweets):
    return [t for t in list_tweets if not 'retweeted_status' in t.keys()]
# Maybe useless
def filter_exception_list(list_tweets):
    exception_list = [
        1003579193907654657, # cemdiasdecodigo
        1003848514823213056, # _30days30sites
    ]
    return [t for t in list_tweets if not t['user']['id'] in exception_list]

## Count filtering
# Convert to dictionary, 'cause reasons
tweets_dict = [json.loads(str(t)) for t in tweets_related]

valid_tweets = filter_retweet(tweets_dict)
valid_tweets = filter_exception_list(valid_tweets)
print(valid_tweets)