from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import esldb
import esldb.models
from scripts import statistics
from translations.models import Translation

def test_esldb_statistics():
    engine = create_engine('sqlite://')
    metadata = esldb.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    _sessionmaker = sessionmaker(engine)

    statistics.esldbstats(_sessionmaker())
