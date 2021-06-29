from sqlalchemy import Column, Integer, String, Text

from .setup import Base


class Joke(Base):
    __tablename__ = 'jokes'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    image = Column(String(250))
