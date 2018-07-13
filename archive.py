import json
filepath = 'ffs_tweets.json'
with open(filepath) as fp:
    for line in fp:
        tweet = json.loads(line)
        id = tweet['id']

        text_file = open('tweets/' + str(tweet['id']) + '.json' , "w")
        text_file.write(json.dumps(tweet, ensure_ascii=False))
        text_file.close()