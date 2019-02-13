import logging
from datetime import datetime
from typing import Dict, List, Union

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


Base: DeclarativeMeta = declarative_base()
logger: logging.Logger = logging.getLogger(__name__)


class AutoCompleteActionEntity(Base):
    __tablename__ = 'autocomplete_action'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    autocomplete_query = Column(String, nullable=False)
    autocomplete_response = Column(JSONB, nullable=False)
    submitted_response = Column(JSONB, nullable=False)
    chat_history = Column(JSONB, nullable=False)


class UserActionLogService(object):
    def __init__(self, db_uri):
        self._db_usi = db_uri
        logger.info('Initializing DB connection pool')
        self._engine = create_engine(db_uri)
        self._create_session = sessionmaker(bind=self._engine)

        logger.info('Attempting to create table(s)')
        Base.metadata.create_all(bind=self._engine, checkfirst=True)
        logger.info('Tables created')

    def persist(
            self,
            autocomplete_query: str,
            autocomplete_response:List[Dict[str,str]],
            submitted_response:Dict[str,Union[str,int]],
            chat_history: List[Dict[str, Union[str, int]]]
    ):
        action = AutoCompleteActionEntity(
            timestamp=datetime.fromtimestamp(submitted_response['timestamp']),
            autocomplete_query=autocomplete_query,
            autocomplete_response=autocomplete_response,
            submitted_response=submitted_response,
            chat_history=chat_history
        )

        logging.info('Serializing action to DB')
        session: Session = self._create_session()
        session.add(action)
        session.flush()
        session.commit()

