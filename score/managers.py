from models import Score
from sqlalchemy.orm.exc import NoResultFound
import logging


logger = logging.getLogger(__name__)


class ScoreManager:

    @classmethod
    def score_from_debt(cls, value):
        return -(value // 20)

    @classmethod
    def score_from_asset(cls, value):
        return (value // 20)

    @classmethod
    def score_from_income(cls, value):
        return (value // 50)

    @classmethod
    def score_func(cls, score_type):
        func_name = f'score_from_{score_type}'

        if hasattr(cls, func_name):
            return getattr(cls, func_name)

        return None

    @classmethod
    def score_from_type(cls, value, score_type):
        func = cls.score_func(score_type)

        if func:
            return func(value)

        logger.warn(f'Not found score calculator to {score_type}.')

        return 0

    @classmethod
    def inc_score(cls, session, cpf, score_type, value):
        score_value = cls.score_from_type(value, score_type)

        logger.info(f'Inc score to {cpf} by {score_value} from type {score_type} and value {value}')

        score = Score()
        score.cpf = cpf
        score.type = score_type
        score.value = value
        score.score = score_value

        session.add(score)
