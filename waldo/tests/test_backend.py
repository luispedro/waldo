from sqlalchemy import create_engine
import waldo.backend

def test_backend():
    assert waldo.backend.Base

def test_create_all():
    metadata = waldo.backend.Base.metadata
    metadata.bind = create_engine('sqlite://')
    metadata.create_all()

