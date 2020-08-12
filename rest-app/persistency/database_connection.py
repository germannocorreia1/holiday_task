from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_errors import InternalConnectionError


def create_connection_with_db(database):
    # Connect to database
    return database.session()


def commit_and_close_database_session(database_session: Session):
    try:
        database_session.commit()
        database_session.close()
    except Exception as e:
        database_session.rollback()
        raise InternalConnectionError
    return
