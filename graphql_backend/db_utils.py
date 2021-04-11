from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker)

engine = create_engine("sqlite:///database/database.db")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_new_comments():
    with engine.connect() as connection:
        result = connection.execute("SELECT COUNT(*) FROM comment WHERE ")