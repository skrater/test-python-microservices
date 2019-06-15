import os
import logging
import sys

import settings
from consumer import start_consumer
from endpoints import start_http

import gevent
from gevent import monkey


monkey.patch_all()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logFormatter = logging.Formatter('[%(asctime)s: %(levelname)s/%(module)s] %(message)s')

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger = logging.getLogger(__name__)

def start():
	logger.info('Starting...')

	jobs = [
		gevent.spawn(start_http),
		gevent.spawn(start_consumer),
	]

	gevent.wait(jobs)


if __name__ == '__main__':
	start()
