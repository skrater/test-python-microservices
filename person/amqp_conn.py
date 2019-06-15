from kombu import Connection
import logging
import settings


logger = logging.getLogger(__name__)
amqp_conn = None


def get_amqp():
	global amqp_conn
	if not amqp_conn:
		logger.info('Connecting to RabbitMQ...')
		amqp_conn = Connection(settings.AMQP_URL)

	return amqp_conn

