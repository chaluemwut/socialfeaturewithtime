# -*- coding: utf-8 -*-

import tweepy, logging, sys, json, os
from pymongo import MongoClient
from datetime import datetime, timedelta

auth = tweepy.AppAuthHandler('8Lh7qrEksDtYT5J521GwIligq', 'i5aRVieT8HJXwfqO6NWEaRCfN0lSF6eKTdRAjBGpUjptAMadKR')
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# search_keyword = ['brexit', 'carnival', 'g7summit','songkran','สงกรานต์', 'oscar2017']

search_keyword = ['หน้ากากทุเรียน', 'themasksinger']

feature = ['retweet_count',
           'favorite_count']

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)

db = client['fwt']

log = logging.getLogger('fwt')
log.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

fh = logging.FileHandler("fwt.log")
fh.setFormatter(format)
log.addHandler(fh)

maxTweets = 10000  # Some arbitrary large number

def load_tweet_since_date(keyword, since_date, unit_date):
    log.info('start key word : ' + keyword)
    no_retweet_count = 0
    tweetCount = 0
    max_id = -1
    sinceId = None
    while tweetCount < maxTweets:
        try:
            log.info('load start...')
            if (max_id <= 0):
                new_tweets = api.search(q=keyword,
                                        since=since_date,
                                        until=unit_date,
                                        exclude_replies=True)
            else:
                new_tweets = api.search(q=keyword,
                                        since=since_date,
                                        until=unit_date,
                                        exclude_replies=True,
                                        max_id=str(max_id - 1))
            if not new_tweets:
                log.info('*********** no more tweet ************')
                break

            for tweet in new_tweets:
                if tweet.retweeted == False and not is_contain_old_tweet(str(tweet.id)):
                    s_data = {}
                    s_data['tweet_id'] = str(tweet.id)
                    s_data['message'] = tweet.text
                    s_data['harvest_keyword'] = keyword
                    s_data['harvest_since_date'] = since_date
                    s_data['harvest_unit_date'] = unit_date
                    db.tweet_search.insert(s_data)
                    no_retweet_count = no_retweet_count + 1

            tweetCount += len(new_tweets)
            log.info("{} : downloaded {} tweets".format(keyword, tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            log.error(str(e))
            log.error('tweet py error')

    return no_retweet_count


def seq_next():
    collection = db.seq
    collection.insert({})
    return collection.count()


def is_contain_old_tweet(tweet_id):
    tweet_db = db.tweet_search.find()
    for tweet_obj in tweet_db:
        if tweet_obj['tweet_id'] == tweet_id:
            return True
    return False


def tweet_search(seq_id, sine_date, unit_date):
    for keyword in search_keyword:
        load_tweet_since_date(keyword, sine_date, unit_date)


def search_by_id(seq_id, sine_date, unit_date):
    log.info('start search by id')
    tweet_result = db.tweet_search.find()
    for db_tweet in tweet_result:
        s_data = {}
        tweet_id = db_tweet['tweet_id']
        try:
            tweet = api.get_status(tweet_id)
            s_data['tweet_id'] = tweet_id
            s_data['harvest_keyword'] = db_tweet['harvest_keyword']
            s_data['retweet_count'] = tweet.retweet_count
            s_data['favorite_count'] = tweet.favorite_count
            s_data['seq_id'] = seq_id
            s_data['sine_date'] = sine_date
            db.tweet_search_id.insert(s_data)
        except Exception as e:
            log.info('error ' + str(e))
    log.info('end search by id')


def process():
    current_date = datetime.now()
    before_date = datetime.now() - timedelta(days=1)

    unit_date = current_date.strftime('%Y-%m-%d')
    sine_date = before_date.strftime('%Y-%m-%d')

    seq_id = seq_next()

    tweet_search(seq_id, sine_date, unit_date)
    search_by_id(seq_id, sine_date, unit_date)


if __name__ == '__main__':
    process()
