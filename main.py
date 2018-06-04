import os
import twitter
from datetime import datetime 

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