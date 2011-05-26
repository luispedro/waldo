from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import re
import gzip

import waldo.backend
import waldo.uniprot.load
import waldo.uniprot.models
import waldo.uniprot.retrieve
import waldo.go.load
import waldo.go.go

from waldo.translations.models import Translation

_testdir = 'tests/data/'
_testfile = _testdir + 'uniprot_sprot.xml.gz'

def load_uniprot_test():
    engine = create_engine('sqlite://')
    metadata = waldo.uniprot.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()

    conn = engine.connect()
    if waldo.backend.use_fts3:
        conn.execute("drop table uniprot_entry")
        conn.execute("CREATE VIRTUAL TABLE uniprot_entry USING fts3 (" +
                "name VARCHAR(32) NOT NULL, " +
                "rname VARCHAR(128) NOT NULL, " +
                "sequence TEXT, " +
                "PRIMARY KEY (name))")

    sessionmaker_ = sessionmaker(engine)
    loaded = waldo.uniprot.load.load(_testdir, sessionmaker_, None)
    session = sessionmaker_()
    return session, loaded

def test_nr_entries():
    nr_entries = len(re.findall('</entry>', gzip.GzipFile(_testfile).read()))
    session,loaded = load_uniprot_test()
    assert loaded == nr_entries
    test_entry = waldo.uniprot.retrieve.retrieve_entry('2AAA_MOUSE', session)
    pubmed_test = "PMID: 17239238 [PubMed - indexed for MEDLINE]"
    doi_test = "PMID: 15489334 [PubMed - indexed for MEDLINE]"

    pubmed_abs = waldo.uniprot.retrieve.retrieve_pubmed_abstract("17239238")
    assert pubmed_abs.endswith(pubmed_test)
    doi_abs = waldo.uniprot.retrieve.retrieve_doi_abstract("10.1101/gr.2596504")
    assert doi_abs.endswith(doi_test)
    assert None == waldo.uniprot.retrieve.retrieve_doi_abstract("not a doi code")

    assert session.query(Translation).filter(and_(Translation.input_namespace == 'ensembl:gene_id', Translation.output_namespace ==  'uniprot:name')).count()
    assert waldo.uniprot.retrieve.from_ensembl_gene_id('ENSMUSG00000007564', session) == '2AAA_MOUSE'
    assert 'GO:0000159' in waldo.uniprot.retrieve.retrieve_go_annotations('2AAA_MOUSE', session)
    assert 'IDA:MGI' in [test_entry.go_annotations[0].evidence_code]
    assert 'Inferred from Direct Assay from MGI' == waldo.uniprot.retrieve.translate_evidence_code('IDA:MGI')
    assert session.query(waldo.uniprot.models.Entry).count() == nr_entries
    entries = waldo.uniprot.retrieve.retrieve_name_matches('subunit', session)
    for ent in entries:
        assert ent.rname.find("subunit") != -1

