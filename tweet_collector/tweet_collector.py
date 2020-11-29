import config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
from pymongo import MongoClient
import time
import logging

# Create a connection to MongoDB
client = MongoClient(host='mongodb', port=27017) # host = name of mongodb container, port = port of container
mongo_db = client.twitter_pipeline
tweet_collection = mongo_db.tweets

def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called credentials.py
       which stores the 4 required authentication tokens:
       1. CONSUMER_API_KEY
       2. CONSUMER_API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET
    """
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """
        Gets called by Tweepy when a new tweet arrives.

        Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) #t is just a regular python dictionary.

        tweet = {
        'username': t['user']['screen_name'],
        'text': t['text'],
        'location': t['user']['location'],
        'followers_count': t['user']['followers_count'],
        'favourites_count':t['user']['favourites_count'],
        'statuses_count': t['user']['statuses_count'],
        'created_at': t['user']['created_at']
        }
        print(t['text'] + '\n\n')

# logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')
# tweet_collection.insert({'username' : tweet['username'],'followers_count' : tweet['followers_count'], 'text' : tweet['text']})
        tweet_collection.insert(tweet)


    def on_error(self, status):

        if status == 420:
            print(status)
            return False

if __name__ == '__main__':

    auth = authenticate()  # log into twitter
    listener = TwitterListener()  # create a listener
    stream = Stream(auth, listener)  # starts an infinite loop  that listens to Twitter
    stream.filter(track=['Germany'], languages=['en'])
