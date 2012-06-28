from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from nose.tools import nottest

def create_sessionmaker(metadata):
    engine = create_engine('sqlite://')
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    return sessionmaker_

testdir = 'waldo/tests/data/'

@nottest
def path_to_testfile(fname):
    from os import path
    return path.join(testdir, fname)
