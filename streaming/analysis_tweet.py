import datetime
import mysql.connector
from redis_database import Redisdb
from textblob import TextBlob

 
with open('mysql_account_inf.txt') as file:
    text = file.read()
    lines = (text.split('\n'))
    mysql_host = lines[0].split(' = ')[1]
    mysql_user = lines[1].split(' = ')[1]
    mysql_passwd = lines[2].split(' = ')[1]
    mysql_database = lines[3].split(' = ')[1]

sqldb = mysql.connector.connect(
	host=mysql_host,
	user=mysql_user,
	passwd=mysql_passwd,
	database=mysql_database
)


redis_db = Redisdb()


while redis_db.get_tweet_data_num() != 0:
	tweet_data_tuple = redis_db.pop_tweet_data()
	
	tweet_data_list = list(tweet_data_tuple)
	tweet_data_str = tweet_data_list[1].decode('utf-8')
	
	tweet_data_str_list = tweet_data_str.split('", "')
	
	tweet_content_dict = {}
	
	for i in tweet_data_str_list:
		i = i.replace('"','').replace('{', '').replace('}','').lstrip().rstrip()
		tweet_content_dict[i.split(':')[0]] = i.split(':')[1].lstrip()

	if tweet_content_dict['place'] != 'None':

		text_analysis_result = TextBlob(tweet_content_dict['text'])
		tweet_content_dict['text_polarity'] = text_analysis_result.sentiment.polarity
		tweet_content_dict['text_subjectivity'] = text_analysis_result.sentiment.subjectivity
		
		if tweet_content_dict['text_polarity'] > 0.7:

			cursor = sqldb.cursor()
			sql_command = 'INSERT INTO Tweet (tweet_user, tweet_text, tweet_text_time) VALUES (%s, %s, %s)'
			val = (tweet_content_dict['id_str'], tweet_content_dict['text'], tweet_content_dict['received_at'])
			cursor.execute(sql_command, val)
			sqldb.commit()
			print('Success: transfer data to Mysql')

