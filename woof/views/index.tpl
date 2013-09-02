<h3>Search by...</h3>
<div style="text-align: center; ">
<table cellspacing="10" cellpadding="10" border="0">
<tr>
    <td>Ensembl gene ID:</td>
    <td>
        <form action="/search/ensemblgene" method="get">
        <input type="text" name="ensemblgene" value="ENSMUSG00000064345" size="32" id="ensemblgene_input" />
        <input type="submit" value="Lookup" />
        </form>
        <script>
        function set_autocomplete(wid, namespace) {
            $.getJSON('{{ get_url('id_list') }}?namespace='+namespace, function (data) {
                $(wid).autocomplete({
                        source: data
                });
            });
        }
        set_autocomplete('#ensemblgene_input', 'ensembl:gene_id');
        </script>
    </td>
</tr>
<tr>
    <td>Ensembl peptide ID:</td>
    <td>
        <form action="/search/ensemblprot" method="get">
        <input type="text" name="ensemblprot" size="32" name='ensemblprot_input' />
        <input type="submit" value="Lookup" />
        </form>
        <script>set_autocomplete('#ensemblgene_input', 'ensembl:peptide_id');</script>
    </td>
</tr>
<tr>
    <td>Uniprot Accession ID:</td>
    <td>
        <form action="/search/uniprotacc" method="get">
        <input type="text" name="uniprotacc" size="32" id='uniprotacc_input' />
        <input type="submit" value="Lookup" />
        </form>
        <script>set_autocomplete('#uniprotacc_input', 'uniprot:accession');</script>
    </td>
</tr>
<tr>
    <td>Uniprot Protein name:</td>
    <td>
        <form action="/search/uniprotname" method="get">
        <input type="text" name="uniprotname" size="32" id='uniprotname_input' />
        <input type="submit" value="Lookup" />
        </form>
        <script>set_autocomplete('#uniprotname_input', 'uniprot:name');</script>
    </td>
</tr>
<tr>
    <td>MGI ID:</td>
    <td>
        <form action="/search/mgiid" method="get">
        <input type="text" name="mgiid" value="MGI:1918918" size="32" id="mgiid_input" />
        <input type="submit" value="Lookup" />
        </form>
        <script>set_autocomplete('#mgiid_input', 'mgi:id');</script>
    </td>
</tr>
<tr>
    <td>LOCATE ID:</td>
    <td>
        <form action="/search/locateid" method="get">
        <input type="text" name="locateid" value="6008510" size="32" id="locateid_input" />
        <input type="submit" value="Lookup" />
        </form>
        <script>set_autocomplete('#locateid_input', 'locate:id');</script>
    </td>
</tr>
</table>
</div>

%rebase base title='Waldo'
