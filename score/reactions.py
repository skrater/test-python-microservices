from topics import subscribe
from sqlalchemy import event
from db import get_session, session_scope
import json
import decimal
from datetime import date
from models import (person_schema, debt_schema,
                    Person, Debt, Asset, Score,
                    Income)
from managers import ScoreManager
from sqlalchemy.orm.exc import NoResultFound
import logging
from producer import send_message


logger = logging.getLogger(__name__)


@subscribe('person.new')
def handle_new_person(payload):
    logger.info(f'Received person.new: {payload}')

    try:
        loaded = person_schema.load(payload)
    except ValidationError as err:
        logger.exception('Invalid payload, ignoring message.')
        return True

    with session_scope() as s:
        s.add(loaded.data)

    return True


@subscribe('debt.new')
def handle_new_debt(payload):
    logger.info(f'Received debt.new: {payload}')

    try:
        loaded = person_schema.load(payload['person'])
    except ValidationError as err:
        logger.error('Invalid payload, ignoring message.')
        return True

    person = loaded.data

    try:
        loaded = debt_schema.load(payload)
    except ValidationError as err:
        logger.error('Invalid payload, ignoring message.')
        return True

    with session_scope() as s:
        debt = loaded.data
        try:
            person = s.query(Person).filter_by(cpf=person.cpf).one()
        except NoResultFound:
            logger.error('Person not found. Retrying...')
            return False

        debt.person = person
        debt.person_id = person.id

        s.add(debt)

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


@event.listens_for(Debt, 'before_insert')
def receive_before_insert_debt(mapper, connection, debt):
    logger.info(f'After insert debt {debt}.')

    @event.listens_for(get_session(), "after_flush", once=True)
    def receive_after_flush(session, context):
        ScoreManager.inc_score(session, debt.person, -(debt.value // 50))


@event.listens_for(Asset, 'before_insert')
def receive_before_insert_asset(mapper, connection, asset):
    logger.info(f'After insert asset {asset}.')

    @event.listens_for(get_session(), "after_flush", once=True)
    def receive_after_flush(session, context):
        ScoreManager.inc_score(session, asset.person, (asset.value // 20))


@event.listens_for(Income, 'before_insert')
def receive_before_insert_asset(mapper, connection, income):
    logger.info(f'After insert income {income}.')

    @event.listens_for(get_session(), "after_flush", once=True)
    def receive_after_flush(session, context):
        ScoreManager.inc_score(session, income.person, (income.value // 50))
