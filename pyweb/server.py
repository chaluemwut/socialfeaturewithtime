from flask import Flask, url_for, session
from flask.templating import render_template
from pymongo import MongoClient
import numpy as np
import os

app = Flask(__name__)

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client['fwt']

search_keyword = ['NorthKorea']


def get_seq():
    col = db.seq
    return col.count()


@app.route("/", methods=['POST', 'GET'])
def index():
    all_data = {}
    last_seq = get_seq()
    for keyword in search_keyword:
        keyword_data_lst = []
        for i in range(1, last_seq + 1):
            list_retweet = []
            list_favorite = []
            db_data_list = db.tweet_search_id.find({'harvest_keyword': keyword, 'seq_id': i})
            for db_data in db_data_list:
                retweet_data = db_data['retweet_count']
                favorite_data = db_data['favorite_count']
                list_retweet.append(retweet_data)
                list_favorite.append(favorite_data)

            if len(list_retweet) == 0:
                av_favorite = 0
            else:
                av_retweet = np.sum(list_retweet)

            if len(list_favorite) == 0:
                av_favorite = 0
            else:
                av_favorite = np.average(list_favorite)

            data_seq_lst = [i, av_retweet, av_favorite, db_data_list.count()]
            keyword_data_lst.append(data_seq_lst)

        all_data[keyword] = keyword_data_lst

    return render_template('index.html', data1=all_data['NorthKorea'])
