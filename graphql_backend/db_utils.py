from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker)

engine = create_engine("sqlite:///database/database.db")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_comments():
    with engine.connect() as connection:
        today = connection.execute("SELECT COUNT(*) FROM comment WHERE date(created_on) > date('now', '-1 days')")
        day_old = connection.execute("SELECT COUNT(*) FROM comment WHERE date(created_on) BETWEEN date('now', '-2 days') AND date('now', '-1 days')")
        all = connection.execute("SELECT COUNT(*) FROM comment")

        return list(today)[0][0], list(day_old)[0][0], list(all)[0][0]


def get_articles():
    with engine.connect() as connection:
        today = connection.execute("SELECT COUNT(*) FROM article WHERE date(created_on) > date('now', '-1 days')")
        day_old = connection.execute("SELECT COUNT(*) FROM article WHERE date(created_on) BETWEEN date('now', '-2 days') AND date('now', '-1 days')")
        all = connection.execute("SELECT COUNT(*) FROM article")

        return list(today)[0][0], list(day_old)[0][0], list(all)[0][0]


def get_articles_count():
    with engine.connect() as connection:
        return list(connection.execute("SELECT COUNT(*) FROM article"))[0][0]


def get_progress():
    with engine.connect() as connection:
        return list(connection.execute("SELECT value FROM progress"))[0][0]
