from flask import Flask, jsonify
import logging
from gevent.pywsgi import WSGIServer
from models import (Person, person_schema, debt_schema,
                    asset_schema, income_schema)
from flask import request
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from db import session_scope


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/person', methods=['POST'])
def new_person():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        with session_scope() as s:
            loaded = person_schema.load(json_data)

            s.add(loaded.data)
    except IntegrityError:
        return jsonify({'message': 'cpf already exists'}), 409
    except ValidationError as err:
        return jsonify(err.messages), 422

    return jsonify({'message': 'created'}), 201


@app.route('/<int:cpf>/debt', methods=['POST'])
def new_debt(cpf):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        with session_scope() as s:
            person = s.query(Person).filter_by(cpf=cpf).one()

            loaded = debt_schema.load(json_data)

            debt = loaded.data
            debt.person = person

            s.add(debt)
    except NoResultFound:
        return jsonify({'message': f'Person with CPF {cpf} could not be found.'}), 400
    except ValidationError as err:
        return jsonify(err.messages), 422

    return jsonify({'message': 'created'}), 201


@app.route('/<int:cpf>/asset', methods=['POST'])
def new_asset(cpf):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        with session_scope() as s:
            person = s.query(Person).filter_by(cpf=cpf).one()

            loaded = asset_schema.load(json_data)

            asset = loaded.data
            asset.person = person

            s.add(asset)
    except NoResultFound:
        return jsonify({'message': f'Person with CPF {cpf} could not be found.'}), 400
    except ValidationError as err:
        return jsonify(err.messages), 422

    return jsonify({'message': 'created'}), 201


@app.route('/<int:cpf>/income', methods=['POST'])
def new_income(cpf):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        with session_scope() as s:
            person = s.query(Person).filter_by(cpf=cpf).one()

            loaded = income_schema.load(json_data)

            income = loaded.data

            income.person = person

            s.add(income)
    except NoResultFound:
        return jsonify({'message': f'Person with CPF {cpf} could not be found.'}), 400
    except ValidationError as err:
        return jsonify(err.messages), 422

    return jsonify({'message': 'created'}), 201


def start_http():
    logger.info('Started http server')

    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
