import csv
import string
import os
import json

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
    1015873697587003392,
    1016073006748233728,
]

exclusion_list = [

]

censor_list = [
    # FFSTechConf Announcements
    1015535398087528449,
    1016990537289732097,
    1016253311522164736,
    1016251590079074304,
    1015568620284411905,
    1015571315955138563,
    1017070440152535040,
    1017341344346460160,
]

def clean_tweet_text(text):
    return text \
        .replace('#FFSTechConf', '') \
        .replace('@FFSTechConf', '') \
        .replace('Anonymised submission:', '') \
        .replace('Anonymised Submission:', '') \
        .strip(string.punctuation) \
        .strip()

def write_csv(filename, tweets):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(['Id', 'Time', 'Text', 'Favourites', 'Retweets', 'Total Mentions','URL'])

        for tweet in tweets:
            writer.writerow([tweet['id'], tweet['created_at'], tweet['text'], tweet['favorite_count'], tweet['retweet_count'], tweet['favorite_count'] + tweet['retweet_count'], 'https://twitter.com/i/web/status/' + str(tweet['id'])])

proposals = {}
not_proposals = {}
censored = {}

count = 0
for f in os.listdir('tweets'):
    file = open('tweets/' + f, 'r')
    tweet = json.loads(file.readline())
    count += 1

    if 'retweeted_status' in tweet.keys():
        tweet = tweet['retweeted_status']

    if tweet['id'] not in proposals.keys() and tweet['id'] not in not_proposals.keys() and tweet['id'] not in censored.keys():
        if tweet['id'] in censor_list:
            censored[tweet['id']] = tweet
        else:
            text = tweet['text']
            cleaned_text = clean_tweet_text(text)

            if tweet['id'] in inclusion_list or (cleaned_text.startswith('FFS') and tweet['id'] not in exclusion_list):
                tweet['text'] = cleaned_text
                proposals[tweet['id']] = tweet
            elif tweet['id'] not in inclusion_list:
                not_proposals[tweet['id']] = tweet

write_csv('proposals.csv', proposals.values())
write_csv('not_proposals.csv', not_proposals.values())
write_csv('censored.csv', censored.values())

print('Total tweets: ' + str(count))