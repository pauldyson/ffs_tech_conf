import tweepy
import yaml
import csv
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

inclusion_list = [
    1016562944144887808,
    1016075751047811073,
    1015714348512305153,
    1016402121686683648,
    1016297776081235969,
    1016058398557732868,
    1016075098242109442,
    1016035574774468614,
    1015573311957426176,
    1016344143168188416,
    1016327741745049601,
    1017033056136368129,
]

exclusion_list = [

]

censor_list = [
    # FFSTechConf Announcements
    1015535398087528449,
    1016990537289732097,
]

proposals = {}
not_proposals = {}
censored = {}

def clean_tweet_text(text):
    return tweet.text \
        .replace('#FFSTechConf', '') \
        .replace('@FFSTechConf', '') \
        .replace('Anonymised submission:', '') \
        .replace('Anonymised Submission:', '') \
        .strip()

def write_csv(filename, tweets):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(['Id', 'Time', 'Text', 'Favourites', 'Retweets', 'Total Mentions','URL'])

        for tweet in tweets:
            writer.writerow([tweet.id, tweet.created_at, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.favorite_count + tweet.retweet_count, 'https://twitter.com/i/web/status/' + str(tweet.id)])


for include in inclusion_list:
    tweet = api.get_status(include)
    tweet.text = clean_tweet_text(tweet.text)
    proposals[tweet.id] = tweet

count = 0

for tweet in tweepy.Cursor(api.search, q="#FFSTechConf").items():
    count += 1
    if hasattr(tweet, 'retweeted_status'):
        tweet = tweet.retweeted_status

    if tweet.id not in proposals.keys() and tweet.id not in not_proposals.keys() and tweet.id not in censored.keys():
        if tweet.id in censor_list:
            censored[tweet.id] = tweet
        else:
            text = tweet.text
            cleaned_text = clean_tweet_text(text)

            if cleaned_text.startswith('FFS') and tweet.id not in exclusion_list:
                tweet.text = cleaned_text
                proposals[tweet.id] = tweet
            elif tweet.id not in inclusion_list:
                not_proposals[tweet.id] = tweet

write_csv('proposals.csv', proposals.values())
write_csv('not_proposals.csv', not_proposals.values())
write_csv('censored.csv', censored.values())

print('Total tweets: ' + str(count))