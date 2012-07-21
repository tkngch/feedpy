#!/usr/bin/env/python2

import sys
import feedparser
import time

from py import config
logger = config.LOGGER
from py.models import Session, Feed, Entry
session = Session()


class Crawler(object):
    def __init__(self):
        self.feeds = []
        subs = config.SUBSCRIPTION
        for section in subs.keys():
            self.feeds.append(Feed(id=section, **subs[section]))

    def crawl(self):
        for source in self.feeds:
            logger.info(source.__repr__())
            try:
                self.parse_feed(source)
            except:
                logger.error(sys.exc_info())
                sys.exc_clear()
        session.commit()

    def parse_feed(self, source):
        raw_feed = feedparser.parse(source.url)
        home_url = raw_feed.get('feed').get('link')

        for raw_entry in raw_feed.entries:
            id = raw_entry.get('id', raw_entry.link)

            if session.query(Entry.id).filter(Entry.id == id).all():
                continue

            author = raw_entry.get('author', '')

            if 'content' in raw_entry:
                content = raw_entry.content[0].value
            elif 'summary' in raw_entry:
                content = raw_entry.summary
            else:
                content = ""

            if 'published_parsed' in raw_entry:
                published = time.mktime(raw_entry.published_parsed)
            else:
                published = 0

            if 'updated_parsed' in raw_entry:
                updated = time.mktime(raw_entry.updated_parsed)
            else:
                updated = 0

            if not updated:
                updated = published
            elif not published:
                published = updated

            author_email = raw_entry.get("author_detail", {}).get("email", "")

            entry = Entry(id=id,
                          source=source.id,
                          url=raw_entry.link,
                          home_url=home_url,
                          author=author,
                          title=raw_entry.title,
                          tag=source.tag,
                          content=content,
                          published=published,
                          updated=updated,
                          author_email=author_email)
            session.add(entry)


def main():
    crawler = Crawler()
    crawler.crawl()


if __name__ == '__main__':
    main()
