from flask import Flask, jsonify
import logging
from gevent.pywsgi import WSGIServer
from models import Person, person_schema, debt_schema
from flask import request, Response
from sqlalchemy.orm.exc import NoResultFound
from db import new_session


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/person', methods=['POST'])
def new_person():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        loaded = person_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    s = new_session()
    s.add(loaded.data)
    s.commit()

    return Response(status=201, mimetype='application/json')


@app.route('/<int:cpf>/debt', methods=['POST'])
def new_debt(cpf):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    s = new_session()

    try:
        person = s.query(Person).filter_by(cpf=cpf).one()
    except NoResultFound:
        return jsonify({'message': f'Person with CPF {cpf} could not be found.'}), 400

    try:
        loaded = debt_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    debt = loaded.data
    debt.person = person

    s.add(debt)
    s.commit()

    return Response(status=201, mimetype='application/json')


def start_http():
    logger.info('Started http server')

    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
