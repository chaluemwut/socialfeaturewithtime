# -*- coding: utf-8 -*-

# alter table all_tweet CHANGE message message VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;


from datetime import datetime, timedelta
from twitter_harvest import TwitterHarvest
from harvest_log import log

def process():
    log.info('begin process..')
    current_date = datetime.now()
    before_date = datetime.now() - timedelta(days=1)

    unit_date = current_date.strftime('%Y-%m-%d')
    sine_date = before_date.strftime('%Y-%m-%d')

    twitter_harvst = TwitterHarvest(sine_date, unit_date)
    twitter_harvst.search_by_keyword()
    twitter_harvst.search_by_id()
    log.info('end process..')


if __name__ == '__main__':
    process()