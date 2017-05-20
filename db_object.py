from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

engine=create_engine('mysql+pymysql://root:Rvpooh123@localhost/sft')

Base = declarative_base()

class KeyWord(Base):
    __tablename__ = 'key_word'
    id = Column(Integer, primary_key=True)
    harvest_keyword = Column(String(5000))
    key_word_type = Column(Integer)
    created_date = Column(DateTime)

class AllTweet(Base):
    __tablename__ = 'all_tweet'
    id = Column(Integer, primary_key=True)
    tweet_id = Column(String(1000))
    message = Column(String(5000))
    harvest_keyword = Column(String(5000))
    harvest_date = Column(DateTime)
    tweet_date = Column(String(1000))

    def __repr__(self):
        return "AllTweet"

class DayTweet(Base):
    __tablename__ = 'day_tweet'
    id = Column(Integer, primary_key=True)
    all_id = Column(Integer, ForeignKey('all_tweet.id'))
    seq_id = Column(Integer)
    retweet_count = Column(Integer)
    poster_user_follower = Column(Integer)
    harvest_date = Column(DateTime)
    tweet_date = Column(String(1000))

    def __repr__(self):
        return "DayTweet"

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)