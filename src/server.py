#!/usr/bin/env python2

import flask
import time
import datetime

from py.models import Session, Entry
from py import config
MAXENTRIES = config.OPTIONS['maxentries']

app = flask.Flask(__name__)


@app.before_request
def connect_db():
    flask.g.session = Session()


_tags = Session().query(Entry.tag.distinct()).all()
tags = ['home'] + list(sorted([_tag[0] for _tag in _tags])) + ['everything']


@app.route('/')
def index():
    return tagged_page('home')


@app.route('/<tag>/')
def tagged_page(tag):
    if (tag in ('home')) or (tag not in tags):
        title = "Today's Feeds"
        today = list(time.localtime())[:3] + [0] * 6
        entries = get_entries(date=time.mktime(today))
        dates = get_dates(entries)
    elif tag in tags:
        title = tag.capitalize() + ' Feeds'
        entries = get_entries(tag=tag)
        dates = get_dates(entries)

    kw = {'tags': tags,
          'title': title,
          'entries': entries,
          'dates': dates}

    return flask.render_template('home.html', **kw)


def get_entries(tag=None, date=None):
    query = flask.g.session.query(Entry)

    if tag and (tag == 'everything'):
        entries = query.order_by(Entry.published.desc())
    elif tag and (tag != 'everything'):
        entries = query.filter(Entry.tag == tag).\
                        order_by(Entry.published.desc()).\
                        limit(MAXENTRIES)
    elif date:
        entries = query.filter(Entry.published >= date).\
                        order_by(Entry.published.desc()).\
                        limit(MAXENTRIES)
    return entries


def get_dates(entries):
    d = {}
    for entry in entries:
        date = time.localtime(entry.published)[0:3]
        d[date] = d.get(date, ()) + (entry,)

    l = d.items()
    l.sort(lambda x, y: -cmp(x[0], y[0]))
    new_dates = {}

    for date, l1 in l:
        new_dates[l1[0]] = datetime.date(*date)

    return new_dates


if __name__ == "__main__":
    app.run(debug=True)
