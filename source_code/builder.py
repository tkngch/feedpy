#! /usr/bin/python2

from flask_frozen import Freezer

from py import config
import server


def main():
    server.app.config['FREEZER_DESTINATION'] = config.OPTIONS['destination']
    server.app.config['FREEZER_BASE_URL'] = config.OPTIONS['baseurl']
    freezer = Freezer(server.app)
    freezer.freeze()

    return freezer


if __name__ == "__main__":
    freezer = main()
    freezer.run(debug=True)
