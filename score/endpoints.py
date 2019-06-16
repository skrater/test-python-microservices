from flask import Flask, jsonify
import logging
from gevent.pywsgi import WSGIServer
from flask import request
from models import Person, person_schema, asset_schema, Score
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError
from db import session_scope


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


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


@app.route('/<int:cpf>/score', methods=['GET'])
def get_score(cpf):
    try:
        with session_scope() as s:
            result = s.query(
                         func.sum(Score.score).label("score_sum")
                     ).join(
                        Person
                     ).filter(
                        Person.cpf==cpf
                     ).first()

            return jsonify({'score': result.score_sum}), 200
    except NoResultFound:
        return jsonify({'message': f'Score from CPF {cpf} could not be found.'}), 404
    except ValidationError as err:
        return jsonify(err.messages), 422


def start_http():
    logger.info('Started http server')

    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
