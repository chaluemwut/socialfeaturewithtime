# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask
from flask.templating import render_template
import os

app = Flask(__name__)

mysql_engine = create_engine('mysql+pymysql://root:Rvpooh123@{}/sft?charset=utf8mb4'.format(os.environ['MYSQL_PORT_27017_TCP_ADDR']))
Session = sessionmaker(bind=mysql_engine)
session = Session()

@app.route("/", methods=['POST', 'GET'])
def index():
    db_result = session.execute("""
    select date(a.harvest_date) as harvest_date, a.harvest_keyword, sum(retweet_count), count(b.all_id)
    from all_tweet a, day_tweet b
    where a.id = b.all_id
    group by date(a.harvest_date), a.harvest_keyword    
        """)
    main_result = []
    for data in db_result:
        main_result.append(data)
        print(data)

    db_date = session.execute("select distinct date(harvest_date) from all_tweet order by date(harvest_date)")
    all_result = {}
    date_list = []
    for date_obj in db_date:
        harvest_date = date_obj[0]
        date_list.append(harvest_date)
        all_data = []
        for data in main_result:
            if data[0] == harvest_date:
                all_data.append(int(data[2]))
        all_result[harvest_date] = all_data

    str = '['
    for harvest_date in date_list[0:2]:
        harvest_result = all_result[harvest_date]
        print(harvest_date, harvest_result)
        str = str+'{'+'"date":"{}", "iran": {}, "mako": {}'.format(harvest_date, harvest_result[0], harvest_result[1])+'},'

    str_result = str[0:-1]+'];'
    print(str_result)
    return render_template('index.html', str_result=str_result)

#
# if __name__ == "__main__":
#     app.run()