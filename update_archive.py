import tweepy
import yaml
import json
from tweepy import OAuthHandler

with open('./oauth.yml', 'r') as stream:
    config = yaml.load(stream)

    consumer_key = config['CONSUMER_KEY']
    consumer_secret = config['CONSUMER_SECRET']
    access_token = config['ACCESS_TOKEN']
    access_secret = config['ACCESS_SECRET']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

count = 0

for tweet in tweepy.Cursor(api.search, q="#FFSTechConf").items():
    count += 1
    text_file = open('tweets/' + str(tweet.id) + '.json', "w")
    text_file.write(json.dumps(tweet._json, ensure_ascii=False))
    text_file.close()