#! /usr/bin/env python2

from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.DB, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Entry(Base):
    __tablename__ = "entry"

    id = Column(String, primary_key=True)
    source = Column(String)
    url = Column(String)
    home_url = Column(String)
    tag = Column(String)
    author = Column(String)
    author_email = Column(String)
    title = Column(String)
    content = Column(String)

    published = Column(Integer)
    updated = Column(Integer)

    new_date = None

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Entry id=%s>" % self.id


class Feed(Base):
    __tablename__ = "feed"

    id = Column(String, primary_key=True)
    url = Column(String)
    tag = Column(String)

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Feed tag=%s id=%s>" % (self.tag, self.id)


Base.metadata.create_all(engine)
