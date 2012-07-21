#!/usr/bin/env python2

__authors__ = (
        'Takao Noguchi'
        )
__license__ = 'GNU General Public License'
__version__ = '2012.07.21'

import argparse


def parse_options():
    parser = argparse.ArgumentParser(description='RSS news aggregator')

    parser.add_argument('--version', action='version',
                        version=__version__)
    parser.add_argument('--crawl', action='store_true',
                        default=False, dest='crawl',
                        help='update the RSS feeds')
    parser.add_argument('--build', action='store_true',
                        default=False, dest='build',
                        help='build static pages')
    parser.add_argument('--serve', action='store_true',
                        default=False, dest='serve',
                        help='crawl and build')

    return parser.parse_args()


def main():
    args = parse_options()

    if args.crawl or args.serve:
        import crawler
        crawler.main()

    if args.build or args.serve:
        import builder
        builder.main()


if __name__ == "__main__":
    main()
