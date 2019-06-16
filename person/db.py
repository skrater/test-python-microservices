from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from models import Base
import logging
import settings


logger = logging.getLogger(__name__)
Session = None
engine = None


def get_engine():
	global engine
	global Session

	if not engine:
		logger.info('Connecting to database...')

		engine = create_engine(settings.RDBMS_URL)
		Session = sessionmaker(bind=engine)

		logger.info('Creating tables...')
		Base.metadata.create_all(engine)

	return engine


def get_session():
	get_engine()

	return Session


def new_session():
	return get_session()()


@contextmanager
def session_scope():
    s = new_session()
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()
