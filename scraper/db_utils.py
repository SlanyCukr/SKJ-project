import datetime
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base_objects import *

engine = create_engine("sqlite:///database/database.db")
Session = sessionmaker(bind=engine)
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def save_article_to_db(session, article: Article):
    fetched_article = session.query(Article).filter_by(link=article.link).scalar()
    if fetched_article is None:
        article.created_on = datetime.datetime.now()
        session.add(article)
        session.commit()
        return article

    return fetched_article


def save_comments(session, comments: [Comment], article: Article):
    updated_comments = []

    for comment in comments:
        fetched_comment = session.query(Comment).filter_by(text=comment.text, author=comment.author).scalar()
        if fetched_comment is None:
            # just set article_id manually, because orm is expensive
            # (if i wouldn't set it manually, it would crash in bulk_save_objects on NULL article_id column)
            comment.article_id = article.id
            comment.created_on = datetime.datetime.now()
            updated_comments.append(comment)
            continue

        if fetched_comment.reactions != comment.reactions:
            fetched_comment.reactions = comment.reactions
            updated_comments.append(fetched_comment)

    session.bulk_save_objects(updated_comments)


def save_to_db(article_data):
    session = Session()

    article = article_data[0]
    authors = article_data[1]
    comments = article_data[2]

    # save article do db
    article = save_article_to_db(session, article)

    # save comments to db
    save_comments(session, comments, article)

    # check if we already have author saved
    for author in authors:
        author_db = session.query(Author).filter(Author.name == author).first()

        # if not, create that author
        if not author_db:
            author_db = Author(name=author, created_on=datetime.datetime.now())
            session.add(author_db)
            session.commit()

        # create linked object between author and article
        if not session.query(ArticleAuthor.id).filter(ArticleAuthor.article_id == article.id, ArticleAuthor.author_id == author_db.id).first():
            session.add(ArticleAuthor(article=article, author=author_db, created_on=datetime.datetime.now()))
            session.commit()


def update_progress(progress: int):
    session = Session()

    progress_object = session.query(Progress).scalar()
    if not progress_object:
        session.add(Progress(value=progress))
    else:
        progress_object.value += progress
        session.add(progress_object)
    session.commit()


def reset_progress():
    session = Session()
    progress_object = session.query(Progress).scalar()
    progress_object.value = 0
    session.commit()
