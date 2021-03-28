from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base_objects import *

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def save_to_db(articles: []):
    session = Session()

    for data in articles:
        article = data[0]
        authors = data[1]
        comments = data[2]

        # save article do db
        session.add(article)
        session.commit()

        # save comments to db
        for comment in comments:
            comment.article = article
        session.add_all(comments)
        session.commit()

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
            session.add(ArticleAuthor(article_id=article.id, author_id=author_id[0]))
            session.commit()
