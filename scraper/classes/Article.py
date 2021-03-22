from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

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
