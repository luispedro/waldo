from waldo.sequences import models

def peptide_sequence(ensembl_peptide, create_session=None):
    '''
    seq = peptide_sequence(ensembl_peptide, create_session={backend.create_session})

    Retrieve amino-acid sequence

    Parameters
    ----------
    ensembl_peptide : str
        Ensembl peptide ID
    create_session : callable, optional
        callable that returns a backend session

    Returns
    -------
    seq : str or None
        If the corresponding ensebl peptide is in the database, returns it as a
        string; otherwise, it returns None.
    '''
    if create_session is None:
        from waldo import backend
        create_session = backend.create_session
    session = create_session()
    seq = session.query(models.EnsemblSequence).filter_by(ensembl_peptide=ensembl_peptide).first()
    if seq is not None:
        return seq.sequence

