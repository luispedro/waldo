from bottle import Bottle, run, template, redirect, static_file, request
from bottle import SimpleTemplate
from bottle import TEMPLATE_PATH

import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve
import waldo.predictions.retrieve
import waldo.sequences.retrieve
import waldo.nog.retrieve
from waldo.translations.services import translate
from waldo.go import id_to_term
import waldo.backend
import json
from os import path

app = Bottle()
route = app.route
SimpleTemplate.defaults["get_url"] = app.get_url

basedir = path.abspath(path.dirname(__file__))
TEMPLATE_PATH.append(path.join(basedir, 'views'))


route('/', name='home', callback=lambda: template('index'))
route('/help', name='help', callback=lambda:template('static/help'))
route('/about', name='about', callback=lambda:template('static/about'))
route('/contact-us', name='contact-us', callback=lambda:template('static/help'))
route('/media/<filename:path>', callback=lambda **f: static_file(f['filename'], root=path.join(basedir,'media')))


@route('/query')
def searchby():
    for key in ('ensemblgene', 'ensemblprot', 'mgiid', 'protname', 'uniprotacc', 'locateid'):
        if key in request.forms:
            value = request.forms.get(key)
            redirect('/search/%s?%s=%s' % (key,key,value))
    redirect('error')


def _result(format, name, value, arguments, predictions=[]):
    if type(arguments) != dict:
        arguments = {'ensemblgene': arguments}
    return template('results', {
            'search_term_type': name,
            'search_term_value': value,
            'all_results': list(_retrieve_all(**arguments)),
            'predictions': predictions,
    })

@route('/search/ensemblgene')
def search(format='html'):
    from collections import defaultdict
    ensemblgene = request.query.ensemblgene

    predictions = waldo.predictions.retrieve.retrieve_predictions(ensemblgene)
    predictions_grouped = defaultdict(list)
    for p in predictions:
        predictions_grouped[p.predictor].append(p)
    predictions = predictions_grouped.items()
    return _result(format, 'Ensembl Gene', ensemblgene, ensemblgene, predictions)


@route('/search/ensemblprot')
def search(format='html'):
    ensemblprot = request.query.ensemblprot
    return _result(format, 'Ensembl Peptide', ensemblprot, {'ensemblpeptide': ensemblprot})

@route('/search/mgiid')
def search(format='html'):
    mgiid = request.query.mgiid
    return _result(format, 'MGI ID', mgiid, translate(mgiid, 'mgi:id', 'ensembl:gene_id'))

@route('/search/uniprotname')
def search(format='html'):
    uniprotname = request.query.uniprotname
    return _result(format, 'Uniprot Name', uniprotname, translate(uniprotname, 'uniprot:name', 'ensembl:gene_id'))

@route('/search/uniprotacc')
def search(format='html'):
    uniprotacc = request.query.uniprotacc
    return _result(format, 'Uniprot Accession ID', uniprotacc, translate(uniprotacc, 'uniprot:accession', 'ensembl:gene_id'))

@route('/search/locateid')
def search(format='html'):
    locateid = request.query.locateid
    return _result(format, 'LOCATE ID', locateid, translate(locateid, 'locate:id', 'ensembl:gene_id'))


def _format(entry, module):
    if module.name == 'LOCATE':
        evidence = '<br />'.join(
                ['<a href="http://locate.imb.uq.edu.au/data_images/%s/%s"><img height="50" width="50" src="http://locate.imb.uq.edu.au/data_images/%s/%s" /></a>' %
                    (img.filename[0:3], img.filename, img.filename[0:3], img.filename) for img in entry.images]),
        location = [(id_to_term(go_id),None) for go_id in module.retrieve_go_annotations(entry.internal_id)]
    else:
        location = [(id_to_term(go_annotation.go_id),go_annotation.evidence_code) for go_annotation in entry.go_annotations]
        try:
            evidence = '<br />'.join((annot.evidence or 'None') for annot in entry.go_annotations),
        except:
            evidence = None
    name = entry.name
    if name is None:
        name = '<unnamed protein>'
    return {
        'protein': name,
        'organism' : '; '.join(map(str,entry.organisms)),
        'celltype': None,
        'condition': None,
        'location': location,
        'references': entry.references,
        'evidence' : evidence,
        'source':'<a href="%s">%s</a>' % (module.retrieve.gen_url(entry.internal_id), module.name),
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
    if op == 'locate':
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

    return HttpResponse(json.dumps(entry, cls=json_entry.EntryEncoder), content_type='application/json')


def main():
    run(app, host='localhost', port=8000)

if __name__ == '__main__':
    main()
