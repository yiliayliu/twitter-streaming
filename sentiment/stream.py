import tweepy
from configparser import SafeConfigParser
import json

parser = SafeConfigParser()
parser.read('stream.cfg')

#This is the super secret information
access_token = parser.get('stream', 'access_token')
access_token_secret = parser.get('stream', 'access_token_secret')
consumer_key = parser.get('stream', 'consumer_key')
consumer_secret = parser.get('stream', 'consumer_secret')

import boto3
aws_key_id =  parser.get('stream', 'aws_key_id')
aws_key =  parser.get('stream', 'aws_key')
DeliveryStreamName = 'PUT-OPS-n4Rjr'
client = boto3.client('firehose', region_name='us-east-1',
						  aws_access_key_id=aws_key_id,
						  aws_secret_access_key=aws_key
						  )

class TweetPrinter(tweepy.Stream):

	def on_status(self, status):
		print(status.id)

	def on_data(self, data):
		print ("tweet arrived!!!")
		print (json.loads(data)["text"] or "NULL")
		client.put_record(DeliveryStreamName=DeliveryStreamName,Record={'Data': json.loads(data)["text"]})
		return True

	def on_error(self, status):
		print ("error!!!")
		print (status)

if __name__ == '__main__':
	stream = TweetPrinter(
				consumer_key,consumer_secret,
				access_token,access_token_secret
			)
	stream.filter(track=['python'])