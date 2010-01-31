from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import go.models
import go.load
import go.go

def test_is_cellular_component():
    engine = create_engine('sqlite://')
    metadata = go.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)

    nr_entries =go.load.load('tests/data/gene_ontology.1_2.obo.gz', sessionmaker_)
    expected = 976 - 79 # instances of "[Term]" - instances of is_obsolete
    assert nr_entries == expected

    session = sessionmaker_ ()
    assert session.query(go.models.Term).count() == nr_entries

    assert go.go.is_cellular_component('GO:0000015')
    assert go.go.is_cellular_component('GO:0000108')
    assert not go.go.is_cellular_component('GO:0000107')

    assert go.go.is_cellular_component('GO:0000015')
    assert go.go.is_cellular_component('GO:0000108')
    assert not go.go.is_cellular_component('GO:0000107')

