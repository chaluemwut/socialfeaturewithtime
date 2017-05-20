# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_object import AllTweet, DayTweet, KeyWord
from datetime import datetime, timedelta
import tweepy, os

from harvest_log import log

auth = tweepy.AppAuthHandler('8Lh7qrEksDtYT5J521GwIligq', 'i5aRVieT8HJXwfqO6NWEaRCfN0lSF6eKTdRAjBGpUjptAMadKR')
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class TwitterHarvest():
    maxTweets = 1000

    def __init__(self, since_date, unit_date):
        self.since_date = since_date
        self.unit_date = unit_date
        mysql_engine = create_engine('mysql+pymysql://root:Rvpooh123@{}/sft?charset=utf8mb4'.format(os.environ['MYSQL_PORT_27017_TCP_ADDR']))
        Session = sessionmaker(bind=mysql_engine)
        self.session = Session()

    def load_tweet_since_date(self, keyword, since_date, unit_date):
        log.info('start key word : ' + keyword)
        no_retweet_count = 0
        tweetCount = 0
        max_id = -1
        sinceId = None
        while no_retweet_count < self.maxTweets:
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
                    if tweet.retweeted == False and not self.is_contain_old_tweet(str(tweet.id)):
                        all_tweet = AllTweet()
                        all_tweet.tweet_id = str(tweet.id)
                        all_tweet.message = tweet.text
                        all_tweet.harvest_keyword = keyword
                        all_tweet.harvest_date = datetime.now()
                        all_tweet.tweet_date = tweet.created_at
                        self.session.add(all_tweet)
                        self.session.commit()

                        no_retweet_count = no_retweet_count + 1

                tweetCount += len(new_tweets)
                log.info("{} : downloaded {} tweets".format(keyword, tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                log.error(str(e))
                log.error('tweet py error')

        return no_retweet_count

    def is_contain_old_tweet(self, tweet_id):
        row_result = self.session.execute("select * from all_tweet where tweet_id = '{}'".format(tweet_id))
        for tweet_obj in row_result:
            return True
        return False

    def get_keyword(self):
        result = []
        row_result = self.session.execute('select * from key_word')
        for r in row_result:
            result.append(r['harvest_keyword'])
        return result

    def search_by_keyword(self):
        for keyword in self.get_keyword():
            self.load_tweet_since_date(keyword, self.since_date, self.unit_date)

    def search_by_id(self):
        log.info('start search by id')
        seq_id = self.next_seq_id()
        tweet_result = self.session.execute("select * from all_tweet")
        for db_tweet in tweet_result:
            tweet_id = db_tweet['tweet_id']
            all_id = db_tweet['id']
            try:
                log.info('start harvest tweet '+tweet_id)
                tweet = api.get_status(tweet_id)
                dayTweet = DayTweet()
                dayTweet.all_id = all_id
                dayTweet.seq_id = seq_id
                dayTweet.retweet_count = tweet.retweet_count
                dayTweet.harvest_date = datetime.now()
                dayTweet.tweet_date = tweet.created_at
                self.session.add(dayTweet)
                self.session.commit()
                log.info('db commit')
            except Exception as e:
                log.info('error ' + str(e))
        log.info('end search by id')

    def next_seq_id(self):
        result = self.session.execute("select count(distinct seq_id)+1 from day_tweet")
        for r in result:
            return r[0]