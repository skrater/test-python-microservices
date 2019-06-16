import logging

import settings
from amqp_conn import get_amqp
from kombu import Connection, Exchange
from kombu.pools import producers

logger = logging.getLogger(__name__)

events_exchange = Exchange(settings.AMQP_EXCHANGE, type='topic')


def send_message(event, message):
    with producers[get_amqp()].acquire(block=True) as p:
        p.publish(message,
                  exchange=settings.AMQP_EXCHANGE,
                  routing_key=event,
                  serializer='json',
                  retry=True,
                  declare=[events_exchange],
                  retry_policy={
                    'interval_start': 1,
                    'interval_step': 1,
                    'errback': errback,
                    'interval_max': 5,
                    'max_retries': 3,
                  })


def errback(exc, interval):
    logger.error('Error from kombu trying to publish a message: %r', exc, exc_info=1)
    logger.info('Retry in %s seconds.', interval)
