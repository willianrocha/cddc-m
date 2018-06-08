import os
from pymongo import MongoClient
from datetime import datetime

TWITTER_DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_URL = os.environ['DB_URL']
URL_DB = DB_URL.format(DB_USER, DB_PASSWORD)

DB_NAME = 'cddc'
C_UDC = 'user_day_count'

def connect_db():
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    db.authenticate(name=DB_USER,password=DB_PASSWORD)
    return db, client

def run_daily(db, tweets):
    status = insert_daily(db, tweets)

def insert_daily(db, tweets):
    udc = db[C_UDC]
    # find better way to update db
    for t in tweets:
        # Check if exists in db
        if udc.find_one({'user_id' : t['user']['id']}) != None:
            # increase counter
            status = udc.update_one({'user_id':t['user']['id']},
                {'$inc': {'work_days': 1}})
        else:
            # Inserto into db
            date = datetime.strptime(t['created_at'], TWITTER_DATE_FORMAT)
            status = udc.insert_one({'user_id': t['user']['id'],
            'screen_name':  t['user']['screen_name'],
            'first_tweet_date': date, 'work_days' : 1, 'reset_counter' : 0})
    # find better way to return the status
    return status

def update_daily(db, tweets):
    udc = db[C_UDC]
    list_id_valid = [id['user']['id'] for id in tweets]
    status = udc.update_many({'user_id' : {'$nin': list_id_valid}},
        {'$inc':{'reset_counter' : 1}})
    return status