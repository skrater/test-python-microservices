from models import Score, Person
from sqlalchemy.orm.exc import NoResultFound
import logging


logger = logging.getLogger(__name__)


class ScoreManager:

    @classmethod
    def inc_score(cls, session, person, value):
        logger.info(f'Inc score from {person} by {value}')

        score = Score()
        score.person = person
        score.score = value

        session.add(score)
