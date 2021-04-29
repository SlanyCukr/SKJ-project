import random

from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker)
from sqlalchemy.exc import OperationalError

engine = create_engine("sqlite:///database/database.db")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def lock_cache(func):
    cached_results = {}

    def func_wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            cached_results[func] = result
            return result
        except OperationalError as e:
            if func in cached_results:
                return cached_results[func]
            return 0
        except Exception as e:
            raise e
    return func_wrapper


@lock_cache
def get_latest_article_id():
    with engine.connect() as connection:
        article = connection.execute("SELECT id FROM article WHERE created_on = (SELECT MAX(created_on) FROM article) LIMIT 1")

        return list(article)[0]
