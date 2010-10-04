from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from waldo.go.models import Term
import waldo.go.load
import waldo.go.go

def test_is_cellular_component():
    engine = create_engine('sqlite://')
    metadata = waldo.go.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    session = sessionmaker_ ()

    nr_entries = waldo.go.load.load('tests/data/', sessionmaker_)
    expected = 976 - 79 # instances of "[Term]" - instances of is_obsolete
    assert nr_entries == expected

    assert session.query(waldo.go.models.Term).count() == nr_entries

    assert waldo.go.go.is_cellular_component('GO:0000015')
    assert waldo.go.go.is_cellular_component('GO:0000108')
    assert not waldo.go.go.is_cellular_component('GO:0000107')

    assert waldo.go.go.is_cellular_component('GO:0000015')
    assert waldo.go.go.is_cellular_component('GO:0000108')
    assert not waldo.go.go.is_cellular_component('GO:0000107')




    id = 'GO:0000015'
    term = 'phosphopyruvate hydratase complex'
    result = waldo.go.go.id_to_term(id, session)
    assert result is not None
    assert result == term

    result = waldo.go.go.term_to_id(term, session)
    assert result is not None
    assert result == id

    id = 'GO:00099999skl'
    term = 'repairosome'
    result = waldo.go.go.id_to_term(id, session)
    assert result == id

    id = 'GO:00099999skl'
    term = 'repairosome'
    result = waldo.go.go.term_to_id(id, session)
    assert result == id


