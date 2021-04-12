from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    link = Column(String)
    header = Column(String)
    description = Column(String)
    category = Column(String)
    published_at = Column(DateTime)
    modified_at = Column(DateTime)
    paragraphs = Column(String)
    created_on = Column(DateTime, server_default=func.now())


class ArticleAuthor(Base):
    __tablename__ = 'article_author'
    id = Column(Integer, primary_key=True)

    article = relationship("Article", backref=backref("article"), lazy=True)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)

    author = relationship("Author", backref=backref("author", lazy=True))
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)

    created_on = Column(DateTime, server_default=func.now())


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_on = Column(DateTime, server_default=func.now())


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    author = Column(String)
    text = Column(String)
    reactions = Column(Integer)

    article = relationship("Article", backref=backref("comment_article", lazy=True))
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
    created_on = Column(DateTime, server_default=func.now())


class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
