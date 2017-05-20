insert into key_word (harvest_keyword, key_word_type, created_date) values ('iran election', 1, now());
insert into key_word (harvest_keyword, key_word_type, created_date) values ('princess mako', 1, now());

alter table all_tweet CHANGE message message VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;


select date(a.harvest_date), a.harvest_keyword, sum(retweet_count), count(b.all_id)
from all_tweet a, day_tweet b
where a.id = b.all_id
group by date(a.harvest_date), a.harvest_keyword;


        var chartData = [{
            "date": "12/08/17",
            "retweet": 230,
			"retweet2": 150
          }, {
            "date": "Poland",
            "retweet": 560,
			"retweet2": 860
        }];