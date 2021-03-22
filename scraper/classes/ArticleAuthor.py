from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class ArticleAuthor(Base):
    __tablename__ = 'article_author'
    id = Column(Integer, primary_key=True)

    article = relationship("Article", backref=backref("article"), lazy=True)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)

    author = relationship("Author", backref=backref("author", lazy=True))
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
