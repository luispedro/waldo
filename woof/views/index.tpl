<p>Type the name of a human or mouse protein:</p>
<form action="/search/uniprotmatch" method="get">
<input type="text" name="q" size="64" id="q" />
<input type="submit" value="Lookup" />
</form>

<h3>Advanced Search</h3>
<p><a href="#" id="expand_advanced">Expand advanced search options...</a></p>
<div id="advanced_search">
<div style="text-align: right; ">
<table cellspacing="10" cellpadding="10" border="0">
<tr>
    <td style="vertical-align: top;">Ensembl gene ID:</td>
    <td>
        <form id="ensemblgene_form" action="/search/ensemblgene" method="get">
        <input type="text" name="ensemblgene" value="" size="32" id="ensemblgene_input" />
        <input type="submit" value="Lookup" />
        </form>
    </td>
</tr>
<tr>
    <td style="vertical-align: top;">Ensembl peptide ID:</td>
    <td>
        <form id="ensemblprot_form" action="/search/ensemblprot" method="get">
        <input type="text" name="ensemblprot" size="32" name='ensemblprot_input' />
        <input type="submit" value="Lookup" />
        </form>
        </script>
    </td>
</tr>
<tr>
    <td style="vertical-align: top;">Uniprot Accession ID:</td>
    <td>
        <form id="uniprotacc_form" action="/search/uniprotacc" method="get">
        <input type="text" name="uniprotacc" size="32" id='uniprotacc_input' />
        <input type="submit" value="Lookup" />
        </form>
    </td>
</tr>
<tr>
    <td style="vertical-align: top;">Uniprot Protein name:</td>
    <td>
        <form id="uniprotname_form" action="/search/uniprotname" method="get">
        <input type="text" name="uniprotname" size="32" id='uniprotname_input' />
        <input type="submit" value="Lookup" />
        </form>
    </td>
</tr>
<tr>
    <td style="vertical-align: top;">MGI ID:</td>
    <td>
        <form id="mgiid_form" action="/search/mgiid" method="get">
        <input type="text" name="mgiid" size="32" id="mgiid_input" />
        <input type="submit" value="Lookup" />
        </form>
    </td>
</tr>
<tr>
    <td style="vertical-align: top;">LOCATE ID:</td>
    <td>
        <form id="locateid_form" action="/search/locateid" method="get">
        <input type="text" name="locateid" size="32" id="locateid_input" />
        <input type="submit" value="Lookup" />
        </form>
    </td>
</tr>
</table>
</div>
</div>
<script>
function set_autocomplete(wid, namespace) {
    $.getJSON('{{ get_url('id_list') }}?namespace='+namespace, function (data) {
        $(wid).autocomplete({
                source: data,
                minLength: 4,
        });
    });
}

function set_sample(wid, value) {
    $('#' + wid).append('<p><a href="#" id="' + wid + '_sample">sample input</a></p>');
    $('#'+wid+'_sample').on('click', function(e) {
        e.preventDefault();
        $('#'+wid+' input[type="text"]').attr('value', value);
        return false;
    });
}
set_sample('ensemblgene_form', 'ENSMUSG00000064345');
set_sample('ensemblprot_form', 'ENSP00000473465');
set_sample('uniprotacc_form', 'P07437');
set_sample('uniprotname_form', 'TBB5_HUMAN');
set_sample('mgiid_form', 'MGI:1918918');
set_sample('locateid_form', '6008510');

set_autocomplete('#q', 'rname');
$('#advanced_search').hide();
$('#expand_advanced').click(function() {
    $('#expand_advanced').hide();
    $('#advanced_search').show();

    set_autocomplete('#ensemblgene_input', 'ensembl:gene_id');
    set_autocomplete('#ensemblgene_input', 'ensembl:peptide_id');
    set_autocomplete('#uniprotacc_input', 'uniprot:accession');
    set_autocomplete('#uniprotname_input', 'uniprot:name');
    set_autocomplete('#mgiid_input', 'mgi:id');
    set_autocomplete('#locateid_input', 'locate:id');

    return false;
});
</script>

%rebase base title='Waldo'
