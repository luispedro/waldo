from collections import defaultdict
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve
import waldo.predictions.retrieve
import waldo.sequences.retrieve
import waldo.nog.retrieve
from waldo.translations.services import translate
import waldo.backend
import json
import json_entry

def searchby(request):
    if request.method == 'GET':
        for key in ('ensemblgene', 'ensemblprot', 'mgiid', 'protname', 'uniprotid', 'locateid'):
            if key in request.GET:
                value = request.GET[key]
                break
        return HttpResponseRedirect('/search/%s/%s' % (key, value))

def search(request, ensemblgene=None, ensemblprot=None, mgiid=None, protname=None, uniprotid=None, locateid=None):
    predictions = None
    if ensemblgene is not None:
        results = _retrieve_all(ensemblgene)
        search_term_type = 'Ensembl gene'
        search_term_value = ensemblgene
        predictions = waldo.predictions.retrieve.retrieve_predictions(ensemblgene)
        predictions_grouped = defaultdict(list)
        for p in predictions:
            predictions_grouped[p.predictor].append(p)
        predictions = predictions_grouped.items()


    elif ensemblprot is not None:
        results = _retrieve_all(ensemblpeptide=ensemblprot)
        search_term_type = 'Ensembl peptide'
        search_term_value = ensemblprot

    elif mgiid is not None:
        results = _retrieve_all(translate(mgiid, 'mgi:id', 'ensembl:gene_id'))
        search_term_type = 'MGI ID'
        search_term_value = mgiid

    elif uniprotid is not None:
        results = _retrieve_all(translate(uniprotid, 'uniprot:name', 'ensembl:gene_id'))
        search_term_type = 'Uniprot ID'
        search_term_value = uniprotid

    elif locateid is not None:
        results = _retrieve_all(translate(locateid, 'locate:id', 'ensembl:gene_id'))
        search_term_type = 'LOCATE ID'
        search_term_value = locateid

    elif protname is not None:
        results = _search_name(protname)
        search_term_type = 'Protein name'
        search_term_value = protname

    return render_to_response(
                'results.html',
                {
                    'search_term_type' : search_term_type,
                    'search_term_value' : search_term_value,
                    'all_results' : list(results),
                    'predictions' : predictions,
                })


def _format(entry, module):
    if module.name == 'LOCATE':
        evidence = '<br />'.join(
                ['<a href="http://locate.imb.uq.edu.au/data_images/%s/%s"><img height="50" width="50" src="http://locate.imb.uq.edu.au/data_images/%s/%s" /></a>' %
                    (img.filename[0:3], img.filename, img.filename[0:3], img.filename) for img in entry.images]),
    else:
        try:
            evidence = '<br />'.join((annot.evidence or 'None') for annot in entry.go_annotations),
        except:
            evidence = '-'
    return {
        'protein': entry.name,
        'organism' : '; '.join(entry.organisms),
        'celltype': '-',
        'condition':'-',
        'location': '; '.join([go_annot.go_id for go_annot in entry.go_annotations]),
        'references': '<br />'.join([paper.title for paper in entry.references]),
        'evidence' : evidence,
        'evidence_code' : '<br />'.join([go_annot.evidence_code for go_annot in entry.go_annotations]),
        'source':'<a href="%s">%s</a>' % (module.retrieve.gen_url(entry.name),module.name),
        }
def _search_name(name):
    session = waldo.backend.create_session()
    uniprot_entries = waldo.uniprot.retrieve.retrieve_name_matches(name, session)
    return [_format(entry, waldo.uniprot) for entry in uniprot_entries]

def _retrieve_all(ensemblgene=None, ensemblpeptide=None):
    '''
    for entry in _retrieve_all(ensemblgene{=None}, ensemblpeptide{=None}):
        ...

    Returns a formatted list of dictionaries, each pertaining to a result from a
    specific database, in a format that can be output as HTML. This function
    behaves as a "least common denominator", using the Ensembl gene or peptide as
    that identifier by which to find all other information across databases.
    '''
    if ensemblgene is None and ensemblpeptide is None:
        return
    session = waldo.backend.create_session()

    for module in (waldo.uniprot, waldo.mgi, waldo.locate):
        if ensemblgene is not None:
            name = module.retrieve.from_ensembl_gene_id(ensemblgene, session)
        else:
            name = module.retrieve.from_ensembl_peptide_id(ensemblpeptide, session)
        if name is None: continue
        entry = module.retrieve.retrieve_entry(name, session)
        if entry is None: continue
        yield _format(entry, module)

def get_json(request, id=None):
    entry = None
    session = waldo.backend.create_session()

    op = request.path_info.split('/')[2]
    if op == 'location' :
        entry = waldo.locate.retrieve.retrieve_entry(id, session)
    elif op == 'uniprot' :
        entry = waldo.uniprot.retrieve.retrieve_entry(id, session)
    elif op == 'sequences' : 
        entry = waldo.sequences.retrieve.peptide_sequence(id, session)
    elif op == 'nog' :
        entry = waldo.nog.retrieve.retrieve_orthologs(id, session)
    elif op == 'predictions' :
        entry = waldo.predictions.retrieve.retrieve_predictions(id, session)
    elif op == 'mgi' :
        entry = waldo.mgi.retrieve.retrieve_entry(id, session)

    return render_to_response('json.html', {
                    'json' : json.dumps(entry, cls=json_entry.EntryEncoder)
                    })
