# import packages
import redis
import json


# define Class
class Redisdb:

	# redis configuration
	redis_host = '127.0.0.1'
	redis_port = '6379'
	redis_pw = ''

	# start a db instance
	def __init__(self):
		self.db = redis.Redis(host=self.redis_host, port=self.redis_port, password=self.redis_pw)

	# save streaming tweet data into Redis list
	def savetweet(self, data):
		self.db.lpush('tweetdata', json.dumps(data))

	# get the length of Redis list
	def get_tweet_data_num(self):
		tweet_data_length = self.db.llen('tweetdata')
		return tweet_data_length

	# peek the element in the Redis list
	def peek_tweet_data(self):
		list_length = self.db.llen('tweetdata')
		tweet_saved_result = self.db.lrange('tweetdata', 0, list_length)
		return tweet_saved_result

	# pop one element feom the Redis list
	def pop_tweet_data(self):
		tweet_data = self.db.brpop('tweetdata')
		return tweet_data
		
