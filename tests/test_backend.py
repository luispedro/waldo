from sqlalchemy import create_engine
import waldo.backend

def test_backend():
    assert waldo.backend.Base
    assert waldo.backend.engine

def test_create_all():
    metadata = waldo.backend.metadata
    metadata.bind = create_engine('sqlite://')
    metadata.create_all()

