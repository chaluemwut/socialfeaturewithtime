# -*- coding: utf-8 -*-
from pymongo import MongoClient
import tweepy, json, os, logging, sys, pickle
import numpy as np

auth = tweepy.AppAuthHandler('9efZotY18bo0IjpmSd4ZQPixa', 'BvrRZOZZ1vMTY8T8Cn4KyJhEkFGFREZtnJbOwiDKZhajiiB4Pp')
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

log = logging.getLogger('harvest')
log.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

fh = logging.FileHandler("harvest.log")
fh.setFormatter(format)
log.addHandler(fh)

def get_by_id(tweet_id):
    try:
        tweet = api.get_status(tweet_id)
        return tweet
    except Exception as e:
        return None

def grap_tweet(tweet_list):
    x = []
    y = []
    tweet_id_lst = []
    for data in tweet_list:
        if data == None:
            continue
        tweet_id = data['tweet_id']
        tweet_obj = get_by_id(tweet_id)
        try:
            x.append(tweet_obj.user.followers_count)
            y.append(tweet_obj.retweet_count)
            tweet_id_lst.append(tweet_id)
            log.info('{}, {}'.format(tweet_obj.user.followers_count, tweet_obj.retweet_count))
        except Exception as e:
            pass
    return x, y, tweet_id_lst

def find_follower():
    client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
    db = client['fwt']

    lt_zone = db.tweet_search_id.find({'retweet_count':{'$lt':5}, 'seq_id': 1})
    x, y, tweet_id = grap_tweet(lt_zone)

    gt_zone = db.tweet_search_id.find({'retweet_count':{'$gt':1000}, 'seq_id': 1})
    x2, y2, tweet_id2 = grap_tweet(gt_zone)

    result = [x, y, tweet_id, x2, y2, tweet_id2]
    pickle.dump(result, open('follower.obj', 'wb'))

def plot_data():
    # import matplotlib.pyplot as plt
    data = pickle.load(open('result/follower.obj', 'rb'))
    for d in data:
        print(d)
    print(np.average(data[0]), len(data[0]))
    print(np.average(data[3]), len(data[3]))
    # plt.boxplot([data[0], data[3]])
    # plt.show()

if __name__ == '__main__':
    json_str = get_by_id('852983633518317568')
    print(json.dumps(json_str._json, indent=4))
    # find_follower()
    # plot_data()
