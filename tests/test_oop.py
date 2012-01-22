import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve
import waldo.predictions.retrieve
import waldo.sequences.retrieve
import waldo.nog.retrieve
from waldo.translations.services import translate
import waldo.backend
from waldo import backend

def test_oop():
    # This just checks that all methods exist &c
    ensemblgene = 'ENSMUSG00000064345'
    session = backend.create_session()
    for module in (waldo.uniprot, waldo.mgi, waldo.locate):
        name = module.retrieve.from_ensembl_gene_id(ensemblgene, session)
        entry = module.retrieve.retrieve_entry(name, session)
        if name is not None and entry is not None:
            if module.name == 'LOCATE':
                evidence = '<br />'.join(
                        ['<a href="http://locate.imb.uq.edu.au/data_images/%s/%s"><img height="50" width="50" src="http://locate.imb.uq.edu.au/data_images/%s/%s" /></a>' %
                            (img.filename[0:3], img.filename, img.filename[0:3], img.filename) for img in entry.images]),
            else:
                try:
                    evidence = '<br />'.join((annot.evidence or 'None') for annot in entry.go_annotations),
                except:
                    evidence = '-'
            d = {
                'protein': entry.name,
                'organism' : '; '.join(entry.organisms),
                'celltype': '-',
                'condition':'-',
                'location': '; '.join(module.retrieve.retrieve_go_annotations(entry.internal_id)),
                'references': '<br />'.join([paper.title for paper in entry.references]),
                'evidence' : evidence,
                'evidence_code' : '<br />'.join([go_annot.evidence_code for go_annot in entry.go_annotations]),
                'source':'<a href="%s">%s</a>' % (module.retrieve.gen_url(entry.name),module.name),
                }
                
