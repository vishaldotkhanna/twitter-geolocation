import json
from math import ceil

import tweepy


# SERVER Credentials
API_KEY = 'pMeSXdld3nEUtFDV5Mp2mXPKj'
API_SECRET_KEY = 'YLHDB81Uoi2LMVcz02niPemZd8I16daoUeC4xFj0LU750f91Mo'
ACCESS_TOKEN = '4915148900-pkG5F5VVpixEnOVdpJgzp1wKnfBORXVKVCHAZMb'
ACCESS_TOKEN_SECRET = 'ygIky10Jkvlzt15fBlIlSqs0dNc9qL7Yuheg14DJyweiD'

BATCH_SIZE = 100
SOURCE_FILE = 'test.tweet'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets = list()


with open(SOURCE_FILE + '.json') as f:
    for record in f:
        tweets.append(json.loads(record.strip()))


def download_tweets():
    total_tweets = len(tweets)
    num_batches = ceil(total_tweets / BATCH_SIZE)
    downloaded_tweets = 0

    print('Total tweets: {}'.format(total_tweets))
    print('Number of batches: {}'.format(num_batches))

    # We only keep some fields for each record
    fields_to_keep = (
    'coordinates', 'created_at', 'geo', 'id', 'lang', 'retweeted', 'retweet_count', 'place', 'user', 'text')

    with open('downloaded_' + SOURCE_FILE + '.json', 'w') as f:
        start = 0
        while start < total_tweets:
            cur_batch_number = int(start / BATCH_SIZE) + 1
            print('Processing batch number {} out of {}'.format(cur_batch_number, num_batches))

            end = min(start + BATCH_SIZE, total_tweets + 1)
            tweet_ids = [tweet['tweet_id'] for tweet in tweets[start:end]]

            try:
                tweets_data = api.statuses_lookup(id_=tweet_ids)
            except Exception as e:
                print('Encountered exception ', e)
                print('Retrying...')
                continue

            downloaded_tweets += len(tweets_data)

            for data in tweets_data:
                data_dict = data._json
                filtered_dict = {field: data_dict[field] for field in fields_to_keep}

                f.write(json.dumps(filtered_dict))
                f.write('\n')

            start = end

    print('Finished downloading')
    print('Successfully downloaded {} tweets out of {}'.format(downloaded_tweets, total_tweets))


if __name__ == '__main__':
    download_tweets()

