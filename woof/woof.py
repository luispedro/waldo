# Woof is part of waldo
# http://murphylab.web.cmu.edu/services/waldo/home

try:
    from bottle import Bottle, run, template, redirect, static_file, request
    from bottle import SimpleTemplate
    from bottle import TEMPLATE_PATH
except:
    from sys import stderr
    stderr.write('''\
import bottle failed. Try

    pip install bottle

See http://bottlepy.org/ for details.''')
    raise

import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve
import waldo.predictions.retrieve
import waldo.sequences.retrieve
import waldo.nog.retrieve
from waldo.translations.services import translate
from waldo.translations.models import namespace_fullname
from waldo.go import id_to_term
import waldo.goslim
import waldo.backend
import json
from os import path

app = Bottle()
route = app.route
SimpleTemplate.defaults["get_url"] = app.get_url

basedir = path.abspath(path.dirname(__file__))
TEMPLATE_PATH.append(path.join(basedir, 'views'))
session = waldo.backend.create_session()

PREDICTIONS_ENABLED = False


route('/', name='home', callback=lambda: template('index'))
route('/help', name='help', callback=lambda:template('static/help'))
route('/about', name='about', callback=lambda:template('static/about'))
route('/contact-us', name='contact-us', callback=lambda:template('static/contact-us'))
route('/media/<filename:path>', callback=lambda **f: static_file(f['filename'], root=path.join(basedir,'media')))



@route('/translate', name='translate', method=('GET','POST'))
def translate_identifiers():
    if 'ids' not in request.forms:
        return template('translate',
            {
                'results': None,
                'namespaces': namespace_fullname.items(),
            })

    inputns = request.forms['inputns']
    outputns = request.forms['outputns']
    results = []
    for i in request.forms['ids'].strip().split():
        i = i.strip()
        if not len(i):
            continue
        e = translate(i, inputns, 'ensembl:gene_id')
        o = translate(e, 'ensembl:gene_id', outputns)
        results.append((i,e,o))

    if format == 'csv':
        return '\n'.join('\t'.join(r) for r in results)
    if format == 'json':
        from collections import namedtuple
        rtype = namedtuple('WaldoIDTranslation', 'input ensembl_gene output')
        results = [rtype(r) for r in results]
        return json.dumps(results)
    return template('translate',
            {   'results': results,
                'inputns_user' : namespace_fullname[inputns],
                'outputns_user' : namespace_fullname[outputns],
                'namespaces': namespace_fullname.items(),
            })

@route('/query')
def searchby():
    for key in ('ensemblgene', 'ensemblprot', 'mgiid', 'protname', 'uniprotacc', 'locateid'):
        if key in request.forms:
            value = request.forms.get(key)
            redirect('/search/%s?%s=%s' % (key,key,value))
    redirect('error')

_mgi_goslim_all = set([
    'cell organization and biogenesis',
    'cytosol',
    'nucleus',
    'other cellular component',
    'ER/Golgi',
    'other membranes',
    'cytoskeleton',
    'plasma membrane',
    'other cytoplasmic organelle',
    'mitochondrion',
    'translational apparatus',
    'extracellular matrix',
    ])

def _result(format, name, value, arguments, predictions=[]):
    if type(arguments) != dict:
        arguments = {'ensemblgene': arguments}
    all_results = []
    goslim = {}
    for entry in _retrieve_all(**arguments):
        all_results.append(entry)
        goslim[entry['module']] = entry['goslim']
    goslim_all = set()
    for g in goslim.values():
        goslim_all.update(g)
    goslim_all = list(goslim_all&_mgi_goslim_all)
    goslim_all.sort()
    return template('results', {
            'search_term_type': name,
            'search_term_value': value,
            'goslim_all' : goslim_all,
            'goslim': goslim,
            'all_results': all_results,
            'predictions': predictions,
            'PREDICTIONS_ENABLED': PREDICTIONS_ENABLED,
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
    if not mgiid.startswith('MGI:'):
        mgiid = 'MGI:'+mgiid
    return _result(format, 'MGI ID', mgiid, translate(mgiid, 'mgi:id', 'ensembl:gene_id'))

@route('/search/uniprotname')
def search(format='html'):
    uniprotname = request.query.uniprotname
    return _result(format, 'Uniprot Name', uniprotname, translate(uniprotname.upper(), 'uniprot:name', 'ensembl:gene_id'))

@route('/search/uniprotacc')
def search(format='html'):
    uniprotacc = request.query.uniprotacc
    return _result(format, 'Uniprot Accession ID', uniprotacc, translate(uniprotacc.upper(), 'uniprot:accession', 'ensembl:gene_id'))

@route('/search/locateid')
def search(format='html'):
    locateid = request.query.locateid
    return _result(format, 'LOCATE ID', locateid, translate(locateid.upper(), 'locate:id', 'ensembl:gene_id'))

_list_cache = {}
@route('/list', name='id_list')
def ensemblgene():
    import json
    namespace = request.query.namespace
    if namespace not in _list_cache:
        from waldo.translations.services import list_all
        full = list_all(namespace)
        full = set(full)
        full = list(full)
        full.sort()
        _list_cache[namespace] = full
    return json.dumps(_list_cache[namespace])

def _format(entry, module):
    if module.name == 'LOCATE':
        evidence = '<br />'.join(
                ['<a href="http://locate.imb.uq.edu.au/data_images/%s/%s"><img height="50" width="50" src="http://locate.imb.uq.edu.au/data_images/%s/%s" /></a>' %
                    (img.filename[0:3], img.filename, img.filename[0:3], img.filename) for img in entry.images]),
        location = [(go_id,None) for go_id in module.retrieve_go_annotations(entry.internal_id)]
    else:
        location = [(go_annotation.go_id,go_annotation.evidence_code) for go_annotation in entry.go_annotations]
        try:
            evidence = '<br />'.join((annot.evidence or 'None') for annot in entry.go_annotations),
        except:
            evidence = None
    name = entry.name
    if name is None:
        name = '<unnamed protein>'
    goslim = [waldo.goslim.map_to_goslim(a, 'mgi') for a,_ in location]
    location = [(id_to_term(loc),ev) for loc,ev in location]
    return {
        'protein': name,
        'organism' : '; '.join(map(str,entry.organisms)),
        'celltype': None,
        'condition': None,
        'location': location,
        'goslim': goslim,
        'module': module.name,
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
    ensemblgene = (ensemblgene.upper() if ensemblgene else ensemblgene)
    ensemblpeptide = (ensemblpeptide.upper() if ensemblpeptide else ensemblpeptide)

    for module in (waldo.uniprot, waldo.mgi, waldo.locate):
        if ensemblgene is not None:
            name = module.retrieve.from_ensembl_gene_id(ensemblgene, session)
        else:
            name = module.retrieve.from_ensembl_peptide_id(ensemblpeptide, session)
        if name is None: continue
        entry = module.retrieve.retrieve_entry(name, session)
        if entry is None: continue
        try:
            yield _format(entry, module)
        except Exception, e:
            print(e)
            pass

def get_json(request, id=None):
    entry = None

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


def main(argv):
    import optparse

    parser = optparse.OptionParser()
    parser.add_option(
                    '--port',
                    action='store',
                    dest='port',
                    help='TCP Port to use (default: 8000)')
    options, args = parser.parse_args(argv)
    if not options.port: options.port = 8000
    run(app, host='localhost', port=options.port)

if __name__ == '__main__':
    from sys import argv
    main(argv)
