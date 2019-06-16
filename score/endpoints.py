from flask import Flask, jsonify
import logging
from gevent.pywsgi import WSGIServer
from models import Score
from sqlalchemy import func
from marshmallow import ValidationError
from db import session_scope


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<int:cpf>/score', methods=['GET'])
def get_score(cpf):
    try:
        with session_scope() as s:
            result = s.query(
                         func.sum(Score.score).label("score_sum")
                     ).filter(
                        cpf==cpf
                     ).first()

            if not result.score_sum:
                return jsonify({'message': f'Score from CPF {cpf} could not be found.'}), 404

            return jsonify({'score': result.score_sum}), 200
    except ValidationError as err:
        return jsonify(err.messages), 422


def start_http():
    logger.info('Started http server')

    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
