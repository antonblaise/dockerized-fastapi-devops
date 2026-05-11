from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from app.database import engine

Base = declarative_base()

class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie = Column(String)
    rating = Column(Integer)
    comment = Column(String)

Base.metadata.create_all(bind=engine)