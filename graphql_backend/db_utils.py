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
        except OperationalError:
            print('Returning cached result, because database is locked.')
            return cached_results[func]
        except Exception as e:
            raise e
    return func_wrapper


@lock_cache
def get_comments():
    with engine.connect() as connection:
        today = connection.execute("SELECT COUNT(*) FROM comment WHERE date(created_on) = date('now')")
        day_old = connection.execute("SELECT COUNT(*) FROM comment WHERE date(created_on) = date('now', '-1 days')")
        all = connection.execute("SELECT COUNT(*) FROM comment")

        return list(today)[0][0], list(day_old)[0][0], list(all)[0][0]


@lock_cache
def get_articles():
    with engine.connect() as connection:
        today = connection.execute("SELECT COUNT(*) FROM article WHERE date(created_on) = date('now')")
        day_old = connection.execute("SELECT COUNT(*) FROM article WHERE date(created_on) = date('now', '-1 days')")
        all = connection.execute("SELECT COUNT(*) FROM article")

        return list(today)[0][0], list(day_old)[0][0], list(all)[0][0]


@lock_cache
def get_authors_count():
    with engine.connect() as connection:
        return list(connection.execute("SELECT COUNT(*) FROM author"))[0][0]


@lock_cache
def get_progress():
    with engine.connect() as connection:
        return list(connection.execute("SELECT value FROM progress"))[0][0]


@lock_cache
def get_grouped_graph_data():
    with engine.connect() as connection:
        comment_counts = list(connection.execute("SELECT COUNT(*) as pocet, date(created_on) FROM comment GROUP BY date(created_on) ORDER BY date(created_on) ASC LIMIT 7"))
        article_counts = list(connection.execute("SELECT COUNT(*) as pocet, date(created_on) FROM article GROUP BY date(created_on) ORDER BY date(created_on) ASC LIMIT 7"))
        return comment_counts, article_counts


@lock_cache
def get_categories():
    with engine.connect() as connection:
        return list(connection.execute("SELECT category, COUNT(*) as pocet FROM article GROUP BY category ORDER BY COUNT(*) DESC"))


@lock_cache
def get_most_frequent_authors():
    with engine.connect() as connection:
        return list(connection.execute("SELECT name, author_id FROM article_author JOIN author ON article_author.author_id = author.id GROUP BY name ORDER BY COUNT(*) DESC LIMIT 7"))


@lock_cache
def get_latest_article_time(author_id):
    with engine.connect() as connection:
        # don't worry about sql injection, because user can't pass data to this app
        return list(connection.execute("SELECT MAX(article.created_on) FROM article JOIN article_author ON article_author.article_id = article.id WHERE author_id = " + str(author_id)))[0][0]


@lock_cache
def get_newest_articles():
    with engine.connect() as connection:
        return list(connection.execute("SELECT link, header, category, created_on, (SELECT COUNT(*) FROM comment WHERE comment.article_id = article.id) FROM article ORDER BY created_on DESC LIMIT 7"))
