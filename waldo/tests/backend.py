from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

def create_sessionmaker(metadata):
    engine = create_engine('sqlite://')
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    return sessionmaker_

