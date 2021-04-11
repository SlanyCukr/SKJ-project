from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base_objects import *

engine = create_engine("sqlite:///../database/database.db")
Session = sessionmaker(bind=engine)
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


def save_article_to_db(session, article: Article):
    fetched_article = session.query(Article).filter_by(link=article.link).scalar()
    if fetched_article is None:
        session.add(article)
        session.commit()
        return article

    return fetched_article


def save_comments(session, comments: [Comment], article: Article):
    for comment in comments:
        fetched_comment = session.query(Comment).filter_by(text=comment.text, author=comment.author).scalar()
        if fetched_comment is None:
            comment.article = article
            session.add(comment)
            continue

        if fetched_comment.reactions != comment.reactions:
            fetched_comment.reactions = comment.reactions
            session.add(fetched_comment)

    session.commit()


def save_to_db(articles: []):
    session = Session()

    for data in articles:
        article = data[0]
        authors = data[1]
        comments = data[2]

        # save article do db
        article = save_article_to_db(session, article)

        # save comments to db
        save_comments(session, comments, article)
        """for comment in comments:
            comment.article = article
        session.add_all(comments)
        session.commit()"""

        # check if we already have author saved
        for author in authors:
            author_id = session.query(Author.id).filter(Author.name == author).first()

            # if not, create that author
            if not author_id:
                author_db = Author(name=author)
                session.add(author_db)
                session.commit()
                author_id = (author_db.id,)

            # create linked object between author and article
            if not session.query(ArticleAuthor.id).filter(ArticleAuthor.article_id == article.id, ArticleAuthor.author_id == author_id[0]).first():
                session.add(ArticleAuthor(article_id=article.id, author_id=author_id[0]))
                session.commit()
