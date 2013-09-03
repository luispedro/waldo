<h2></h2>
<p>Results for <cite>{{ search_term_value }}</cite></p>

<p>See results for <input type="checkbox" checked="true" id="see_human" /> Human
<input type="checkbox" checked="true" id="see_mouse" /> Mouse</a>
<p id="no_data" style="color: #f90">You have selected no rows.</p>
<script>$('#no_data').hide();</script>
<table>
<tr>
<th>Uniprot Name</th>
<th>Name</th>
</tr>
% for e in results:
    <tr class="{{ ('human_tr' if e.name.endswith('HUMAN') else 'mouse_tr') }}">
    <td><a href="/search/uniprotname?uniprotname={{e.name}}">{{ e.name  }}</a></td>
    <td style="padding-left: 2em"><a href="/search/uniprotname?uniprotname={{e.name}}">{{ e.rname }}</a></td>
    </tr>
% end
</table>

<script>
function update_no_data() {
    if (!$('#see_human').prop('checked')  && !$('#see_mouse').prop('checked')) {
        $('#no_data').show();
    } else {
        $('#no_data').hide();
    }
}
$('#see_human').change(function() {
    update_no_data();
    if ($('#see_human').prop('checked')) {
        $('.human_tr').show();
    } else {
        $('.human_tr').hide();
    }
});
$('#see_mouse').change(function() {
    update_no_data();
    if ($('#see_mouse').prop('checked')) {
        $('.mouse_tr').show();
    } else {
        $('.mouse_tr').hide();
    }
});
</script>

% rebase base title='Waldo'
