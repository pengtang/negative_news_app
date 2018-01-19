import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Text, BigInteger, Float
from math import ceil

Base = declarative_base()


class RelatedArticles(Base):
    """
    This table stores data coming from google search api
    """
    # TODO: Maybe add some fields, e.g. author, keywords

    __tablename__ = "related_articles"

    link                = Column(Text, primary_key=True)
    created_date        = Column(DateTime, default=datetime.datetime.utcnow)
    title               = Column(Text)
    keyword_searched    = Column(Text)
    text                = Column(Text)
    related_probability = Column(Float)

    def __init__(self, link, title, keyword_searched, text, related_probability):
        self.link = link
        self.title = title
        self.keyword_searched = keyword_searched
        self.text = text
        self.related_probability = related_probability

    def __repr__(self):
        return '<User %r>' % self.link


# # TODO: Still unfinished
# class RelatedTweets(Base):
#     """
#     This table stores data coming from tweets(twitter)
#     """
#
#
#     __tablename__ = "related_tweets"
#
#     tweet_id = Column(Text)
#     twitter_user_id = Column(BigInteger)
#     source = Column(Text)
#
#     tweet_datetime = Column(DateTime, default=datetime.datetime.utcnow)
#     text = Column(Text)
#     language = Column(Text)


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num