import boto3
import json
from datetime import datetime
import calendar
import random
import time
import sys
# from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from configparser import SafeConfigParser

#Variables that contains the user credentials to access Twitter API
parser = SafeConfigParser()
parser.read('../stream.cfg')

#This is the super secret information
access_token = parser.get('stream', 'access_token')
access_token_secret = parser.get('stream', 'access_token_secret')
consumer_key = parser.get('stream', 'consumer_key')
consumer_secret = parser.get('stream', 'consumer_secret')

aws_key_id =  parser.get('stream', 'aws_key_id')
aws_key =  parser.get('stream', 'aws_key')
stream_name = 'twitter-covid'  # fill the name of Kinesis data stream you created
# create kinesis client connection
kinesis_client = boto3.client('firehose',
                                region_name='us-east-1',  # enter the region
                                aws_access_key_id=aws_key_id,  # fill your AWS access key id
                                aws_secret_access_key=aws_key)  # fill you aws secret access key

class TweetStream(Stream):        
    # on success
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            if 'text' in tweet.keys():
                #print (tweet['text'])
                # message = str(tweet)+',\n'
                message = json.dumps(tweet)
                message = message + ",\n"
                print(message+"=====new version\n")
                kinesis_client.put_record(
                    DeliveryStreamName=stream_name,
                    Record={
                    'Data': message
                    }
                )
        except (AttributeError, Exception) as e:
                print (e)
        return True
        
    # on failure
    def on_error(self, status):
        print(status)



if __name__ == '__main__':
    # create instance of the tweepy tweet stream listener
    stream = TweetStream(consumer_key,consumer_secret,
				access_token,access_token_secret)
    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # create instance of the tweepy stream
    # stream = Stream(auth, listener)
    # search twitter for tags or keywords from cli parameters
    query = sys.argv[1:] # list of CLI arguments 
    query_fname = ' '.join(query) # string
    stream.filter(track=query)

