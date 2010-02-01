from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import re

import uniprot.load
import uniprot.models
import uniprot.retrieve
from translations.models import Translation

_testinput = 'tests/data/uniprot_small.xml'

def test_nr_entries():
    nr_entries = len(re.findall('</entry>', file(_testinput).read()))

    engine = create_engine('sqlite://')
    metadata = uniprot.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    uniprot.load.load(_testinput, sessionmaker_)
    session = sessionmaker_()
    assert session.query(uniprot.models.Entry).count() == nr_entries
    assert session.query(Translation).filter(and_(Translation.input_namespace == 'ensembl:gene_id', Translation.output_namespace ==  'uniprot:name')).count()
    assert uniprot.retrieve.from_ensembl_gene_id('ENSMUSG00000007564') == '2AAA_MOUSE'
    assert 'GO:0005829' in uniprot.retrieve.retrieve_go_annotations('2AAA_MOUSE')
