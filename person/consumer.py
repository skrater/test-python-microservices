from kombu import Exchange, Queue, binding
import settings
import logging
from topics import Topic
import reactions # Subscribe all topics
from amqp_conn import get_amqp


logger = logging.getLogger(__name__)


def process_event(body, message):
    routing_key = message.delivery_info.get('routing_key')

    success = Topic(routing_key).publish(body)

    if not success:
        logger.info(f'Failed to process topic {routing_key}. Requeue message.')

        message.nack()
        return

    message.ack()


def start_consumer():
    connection = get_amqp()

    exchange = Exchange(settings.AMQP_EXCHANGE, 'topic', durable=True)

    receivers = Topic.receivers()
    bindings = []

    for r in receivers:
        logger.info(f'Subscribing {r} to queue {settings.AMQP_QUEUE}.')

        bindings.append(binding(exchange, routing_key=r))

    queue = Queue(name=settings.AMQP_QUEUE, exchange=exchange, bindings=bindings)

    with connection.Consumer([queue],
                             callbacks=[process_event]) as consumer:
        logger.info('Started consumer. Consuming messages...')

        while True:
            connection.drain_events()
