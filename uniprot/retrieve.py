import backend
from translations.models import Translation
from sqlalchemy import and_
from uniprot.models import Entry

def from_ensembl_gene_id(ensembl_gene_id, session=None):
    '''
    name = from_ensembl_gene_id(ensembl_gene_id, session={backend.create_session()})

    Convert ensembl_gene_id to uniprot name (uniprot ID).

    Parameters
    ----------
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      name : uniprot gene name
    '''
    if session is None:
        session = backend.create_session()
    trans = session.query(Translation).filter(
                    and_(Translation.input_namespace == 'ensembl:gene_id',
                    Translation.input_name == ensembl_gene_id,
                    Translation.output_namespace ==  'uniprot:name')).first()
    return trans.output_name

def retrieve_go_annotations(name, session=None):
    '''
    go_ids = retrieve_go_annotations(name, session={backend.create_session()})

    Retrieve GO ids by uniprot name.

    Parameters
    ----------
      name : uniprot name
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      go_ids : list of go terms (of the form "GO:00...")
    '''
    if session is None: session = backend.create_session()
    entr = session.query(Entry).filter(Entry.name == name).first()
    return [go.go_id for go in entr.go_annotations]
