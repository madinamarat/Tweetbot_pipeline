'''
Python module that
1) Extracts Data From the MongoDB database
- Connect to the database
- Query the data
2) Transforms the data
- Perform sentiment analysis
3) Loads the data into a Postgres database
- Connect to the database
- Create table(s)
- INSERT INTO
'''

import time
import logging
from pymongo import MongoClient
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

time.sleep(20)

# Connect to the MongoDB database
client = MongoClient(host='mongodb', port=27017)
mongo_db = client.twitter_pipeline
tweet_collection = mongo_db.tweets

# Connect to the Postgres database
HOST = 'mypg'
USERNAME = 'postgres'
PORT = '5432'
DB = 'postgres'
PASSWORD = '1234'

engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}',pool_size=10, max_overflow=20)

# Create table tweets in the Postgres database
CREATE_QUERY = ''' CREATE TABLE IF NOT EXISTS tweets
                   (name VARCHAR(50),
                   text VARCHAR(500),
                   location VARCHAR(100),
                   followers_count NUMERIC,
                   favourites_count NUMERIC,
                   statuses_count NUMERIC,
                   created_at VARCHAR(50),
                   sentiment_score NUMERIC);'''
engine.execute(CREATE_QUERY)

#Instantiate Vader
s = SentimentIntensityAnalyzer()

# Write functions for each step of the ETL process
def extract():
    '''Extracts tweets from the MongoDB database'''
    tweets = list(tweet_collection.find())[-2:] # The [-2:] ensures that only the last two tweets are extracted
    # tweets is a list of tweets, where each item is a tweet. Each tweet is of the datatype dict or cursor
    return tweets

def transform(tweets):
    '''
    Transform tweets that were extracted from MongoDB
    Parameters:
    -----------
    tweets : List of tweets that were extracted from the MongoDB database.
    '''
    for tweet in tweets:
        # tweet is a dictionary which is a mutable object
        # when saying tweet['sentiment_score'] = 1, we add a key value pair to the dictionary tweet
        # E.g. tweet is {'username': 'Diana', 'text':'This was a long lecture'}
        tweet['sentiment_score'] = s.polarity_scores(tweet['text'])['compound']
    return tweets

def load(tweets):
    '''
    Load transformed tweets into the Postgres database

    Parameters:
    -----------
    tweets : List of tweets that were extracted from the MongoDB database and transformed.
    '''
    insert_query = 'INSERT INTO tweets VALUES (%s, %s, %s,%s,%s,%s, %s,%s)'
    for tweet in tweets:
        engine.execute(insert_query, (tweet['username'], tweet['text'], tweet['location'], tweet['followers_count'], tweet['favourites_count'], tweet['statuses_count'], tweet['created_at'], tweet['sentiment_score']))

while True:
    time.sleep(10)
    extracted_tweets = extract()
    transformed_tweets = transform(extracted_tweets)
    load(transformed_tweets)
    logging.warning('---New list of tweets has been written into the Postgres database')

'''
Suggestion:
- Right now, the whole collection of tweets is queried completely every time the ETL process runs.
- This will lead to duplicates in the Postgres database
- One suggestion was to delete a tweet from the MongoDB databse after querying it. That way you
make sure to not have duplicates
- You could use timestamps to only query the newest tweets
- You could mark tweets that have been extracted as extracted (tweet_collection.update_many())
'''
