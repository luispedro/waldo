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
                    'all_results' : results,
                    'predictions' : predictions,
                })

def _search_name(name):
    session = waldo.backend.create_session()
    uniprot_entries = waldo.uniprot.retrieve.retrieve_name_matches(name, session)
    res = []
    if uniprot_entries is not None:
        for uniprot_entry in uniprot_entries:
            if(uniprot_entry is None):
                continue
            res.append({
                    'protein' : uniprot_entry.name,
                    'organism': '; '.join([organism.organism for organism in uniprot_entry.organisms]),
                    'celltype':'-',
                    'condition':'-',
                    'location': '; '.join([go_annot.go_id for go_annot in uniprot_entry.go_annotations]),
                    'references': '<br />'.join([paper.title for paper in uniprot_entry.references]),
                    'evidence':'<br />'.join([comment.text for comment in uniprot_entry.comments]),
                    'evidence_code' : '<br />'.join([waldo.uniprot.retrieve.translate_evidence_code(go_annot.evidence_code) for go_annot in uniprot_entry.go_annotations]),
                    'source':'<a href="%s">Uniprot</a>' % waldo.uniprot.retrieve.gen_url(uniprot_entry.name),
                    })

    return res

def _retrieve_all(ensemblgene=None, ensemblpeptide=None):
    '''
    list = _retrieve_all(ensemblgene{=None}, ensemblpeptide{=None})

    Returns a formatted list of dictionaries, each pertaining to a result from a
    specific database, in a format that can be output as HTML. This function
    behaves as a "least common denominator", using the Ensembl gene or peptide as
    that identifier by which to find all other information across databases.
    '''
    if ensemblgene is None and ensemblpeptide is None: return None
    session = waldo.backend.create_session()

    # pull out the database-specific IDs
    if ensemblgene is not None:
        uniprot_name = waldo.uniprot.retrieve.from_ensembl_gene_id(ensemblgene, session)
        mgi_id = waldo.mgi.retrieve.from_ensembl_gene_id(ensemblgene, session)
        locate_id = waldo.locate.retrieve.from_ensembl_gene_id(ensemblgene, session)
    else:
        uniprot_name = waldo.uniprot.retrieve.from_ensembl_peptide_id(ensemblpeptide, session)
        locate_id = waldo.locate.retrieve.from_ensembl_peptide_id(ensemblpeptide, session)
        mgi_id = waldo.mgi.retrieve.from_ensembl_peptide_id(ensemblpeptide, session)

    # create objects
    uniprot_entry = waldo.uniprot.retrieve.retrieve_entry(uniprot_name, session)
    mgi_entry = waldo.mgi.retrieve.retrieve_entry(mgi_id, session)
    locate_entry = waldo.locate.retrieve.retrieve_entry(locate_id, session)

    # for each object, put in correct format
    res = []
    if uniprot_entry is not None:
        res.append({
                'protein' : uniprot_entry.name,
                'organism': '; '.join([organism.organism for organism in uniprot_entry.organisms]),
                'celltype':'-',
                'condition':'-',
                'location': '; '.join([go_annot.go_id for go_annot in uniprot_entry.go_annotations]),
                'references': '<br />'.join([paper.title for paper in uniprot_entry.references]),
                'evidence':'<br />'.join([comment.text for comment in uniprot_entry.comments]),
                'evidence_code' : '<br />'.join([go_annot.evidence_code for go_annot in uniprot_entry.go_annotations]),
                'source':'<a href="%s">Uniprot</a>' % waldo.uniprot.retrieve.gen_url(uniprot_name),
                })
    if mgi_entry is not None:
        res.append({
                'protein': mgi_entry.name,
                'organism':'Mus Musculus',
                'celltype':'-',
                'condition':'-',
                'location':'; '.join(waldo.mgi.retrieve.retrieve_go_annotations(mgi_id)),
                'references': mgi_entry.pubmedids != None and '<br />'.join('<a href="http://www.ncbi.nlm.nih.gov/pubmed/%s">%s</a>' % (pubmedid, pubmedid) for pubmedid in mgi_entry.pubmedids.split('|')) or 'None',
                'evidence': '<br />'.join([annot.evidence and annot.evidence or 'None' for annot in mgi_entry.annotations]),
                'evidence_code' : '-',
                'source':'<a href="%s">MGI</a>' % waldo.mgi.retrieve.gen_url(mgi_entry.mgi_id),
                })
    if locate_entry is not None:
        res.append({
                'protein': '%s (%s)' % (locate_entry.accn, locate_entry.source_name),
                'organism': locate_entry.organism,
                'celltype': '-',
                'condition': '-',
                'location': '; '.join(waldo.locate.retrieve.retrieve_go_annotations(locate_id)),
                'references':'<br />'.join([ref.title for ref in locate_entry.references]),
                'evidence': '<br />'.join(['<a href="http://locate.imb.uq.edu.au/data_images/%s/%s"><img height="50" width="50" src="http://locate.imb.uq.edu.au/data_images/%s/%s" /></a>' % (img.filename[0:3], img.filename, img.filename[0:3], img.filename) for img in locate_entry.images]),
                'evidence_code' : '-',
                'source':'<a href="%s">LOCATE</a>' % waldo.locate.retrieve.gen_url(locate_id),
                })
    return res

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



    return render_to_response('json.html', {'json' : json.dumps(entry, cls=json_entry.EntryEncoder)})
