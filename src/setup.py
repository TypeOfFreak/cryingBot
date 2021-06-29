from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def connect():
    engine = create_engine('sqlite:///data/cry.db')
    Base.metadata.create_all(engine)

    Base.metadata.bind = engine

    db_session = sessionmaker(bind=engine)
    # Экземпляр DBSession() отвечает за все обращения к базе данных
    # и представляет «промежуточную зону» для всех объектов,
    # загруженных в объект сессии базы данных.
    return db_session()
