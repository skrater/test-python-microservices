from topics import subscribe
from sqlalchemy import event
from db import get_session, session_scope
import json
import decimal
from datetime import date
from managers import ScoreManager
import logging
from producer import send_message


logger = logging.getLogger(__name__)


def inc_score(score_type, payload):
    with session_scope() as s:
        cpf = payload['person']['cpf']
        value = payload['value']

        score = ScoreManager.new_score(cpf, score_type, value)

        s.add(score)


@subscribe('debt.new')
def handle_new_debt(payload):
    logger.info(f'Received debt.new: {payload}')

    inc_score('debt', payload)

    return True


@subscribe('asset.new')
def handle_new_asset(payload):
    logger.info(f'Received asset.new: {payload}')

    inc_score('asset', payload)

    return True


@subscribe('income.new')
def handle_new_incoe(payload):
    logger.info(f'Received income.new: {payload}')

    inc_score('income', payload)

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
    for obj in session.new:
        if not obj.event_name:
            continue

        logger.info(f'Seding to RabbitMQ {obj}.')

        send_message(f'{obj.event_name}.new', obj.as_json)
