import os
from pymongo import MongoClient, UpdateMany, UpdateOne
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

# Broken
def update_challengers(db, tweets):
    udc = db[C_UDC]
    list_id_valid = [id['user']['id'] for id in tweets]
    increment_work_days = UpdateMany(
        {'user_id' : {'$in':list_id_valid}},
        {'$inc': {'work_days': 1}})
    increment_reset_counter = UpdateMany(
        {'user_id' : {'$nin':list_id_valid}},
        {'$inc': {'reset_counter': 1}})
    insert_new = [UpdateOne(
        {'user_id' : {'$nin':list_id_valid}},
        {'$set': {
            'user_id': t['user']['id'],
            'screen_name':  t['user']['screen_name'],
            'first_tweet_date': datetime.strptime(t['created_at'],
                TWITTER_DATE_FORMAT),
            'work_days' : 1,
            'reset_counter' : 0
        }}, upsert=True) for t in tweets]
    requests = [increment_work_days, increment_reset_counter] + insert_new
    status = udc.bulk_write(requests)
    return status

def warn_user(db, days):
    udc = db[C_UDC]
    call_users = udc.find({'reset_counter' : {'$gt': days}})
    if call_users != None:
        call_users = [c for c in call_users]
    return call_users