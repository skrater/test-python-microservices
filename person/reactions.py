from topics import subscribe
from sqlalchemy import event
from db import get_session
import json
import decimal
from datetime import date
import logging
from producer import send_message


logger = logging.getLogger(__name__)


@subscribe('person.new')
def handle_new_person(payload):
    logger.info(f'Received person.new: {payload}')

    return True


@subscribe('debt.new')
def handle_new_debt(payload):
    logger.info(f'Received debt.new: {payload}')

    return True


class EncoderJSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()

        if isinstance(obj, decimal.Decimal):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


@event.listens_for(get_session(), 'after_flush')
def receive_after_flush(session, flush_context):
    logger.info('After session flush.')

    for obj in session.new:
        logger.info(f'Seding to amqp {obj}.')

        send_message(obj.event_name, obj.as_json)
