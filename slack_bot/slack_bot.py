import time
import slack
import logging
from sqlalchemy import create_engine
import config

#Postgres
HOST = 'mypg'
USERNAME = 'postgres'
PORT = '5432'
DB = 'postgres'
PASSWORD = '1234'
engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}',pool_size=10, max_overflow=20)

def extract():
    tweet_list = []
    query = '''SELECT text, sentiment_score FROM tweets'''
    query_result=engine.execute(query)
    for i in query_result:
        tweet_list.append(i)
    return tweet_list

def bot(tweet_list):
    client = slack.WebClient(token = config.oauth_token)
    for tweet in tweet_list:
        response = client.chat_postMessage(channel='#botchannel', text=f"new tweet: {tweet}")

while True:
    time.sleep(60)
    extracted_tweets = extract()
    bot(extracted_tweets)
    logging.warning('---New tweet has been sent to slackbot ')
