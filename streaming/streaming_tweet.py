import datetime
import tweepy
from redis_database import Redisdb


with open('tweet_api.txt') as file:
    text = file.read()
    lines = (text.split('\n'))
    consumer_api_key = lines[0].split(' = ')[1]
    consumer_api_secret_key = lines[1].split(' = ')[1]
    access_token = lines[2].split(' = ')[1]
    access_token_secret = lines[3].split(' = ')[1]


auth = tweepy.OAuthHandler(consumer_api_key, consumer_api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


redis_obj = Redisdb()


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if 'RT @' not in status.text:
            tweet_item = {
                'id_str': status.id_str,
                'text': status.text,
                'received_at': datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                'place': str(status.place),
            }
            
            redis_obj.savetweet(tweet_item)


stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

stream.filter(languages=['en'], track=['melbourne', 'restaurant'])
