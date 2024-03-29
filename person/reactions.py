from sqlalchemy import event
from db import get_session
import json
import decimal
from datetime import date
import logging
from producer import send_message


logger = logging.getLogger(__name__)


class EncoderJSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()

        if isinstance(obj, decimal.Decimal):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


@event.listens_for(get_session(), 'after_flush')
def receive_after_flush(session, flush_context):
    for obj in session.new:
        if not obj.event_name:
            continue

        logger.info(f'Seding to RabbitMQ {obj}.')

        send_message(f'{obj.event_name}.new', obj.as_json)
