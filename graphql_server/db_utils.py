from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker)

engine = create_engine("sqlite:///../scraper/database.db")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
