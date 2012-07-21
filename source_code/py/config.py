#!/usr/bin/env python2

import os
import sys
import logging
import ConfigParser


def _read_conf():
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
    configfile = 'feedpy/feedpy.conf'
    subscriptionfile = 'feedpy/subscription'
    if xdg_config_home:
        user_conf = os.path.join(xdg_config_home, configfile)
        user_subs = os.path.join(xdg_config_home, subscriptionfile)
    else:
        user_conf = os.path.join(os.path.expanduser('~'),
                                 '.config', configfile)
        user_subs = os.path.join(os.path.expanduser('~'),
                                 '.config', subscriptionfile)

    parser_conf = ConfigParser.RawConfigParser()
    parser_subs = ConfigParser.RawConfigParser()
    if os.path.exists(user_conf):
        parser_conf.read(user_conf)
        parser_subs.read(user_subs)
    else:
        sys.exit('config file not found.')

    return _sort_parsed(parser_conf), _sort_parsed(parser_subs)


def _sort_parsed(parser):
    parsed = dict((section, dict(parser.items(section)))
                    for section in parser.sections())
    return parsed


def _set_logger():
    LOGFILE = '%s/feedpy/feedpy.log' % os.environ.get('XDG_DATA_HOME')
    logger = logging.getLogger()

    handler = logging.FileHandler(LOGFILE)
    formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s line %(lineno)d \t %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


_conf = _read_conf()
OPTIONS = _conf[0]['Options']
SUBSCRIPTION = _conf[1]

LOGGER = _set_logger()

DATABASE = '%s/feedpy/feedpy.db' % os.environ.get('XDG_DATA_HOME')
DB = 'sqlite:///%s' % DATABASE
