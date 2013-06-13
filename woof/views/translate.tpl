<h2>Identifier Translation</h2>
<form action="/translate" method="post">
<p><label for="inputns">Input Namespace:</label> <select name="inputns" id="inputns">
%for (code,ns) in namespaces:
    <option name="{{code}}">{{ns}}</option>
%end
        </select>
<p>Input your identifiers (max 100):
<p><textarea rows="20" cols="50" name="ids" id="ids">
</textarea>
<p><a href="#" id="samplebutton">Try with sample input</a></p>
<script>
$('#samplebutton').click(function() {
    $('textarea#ids').val('ENSG00000075624');
    return false;
});
</script>
<p><label for="outputns">Output Namespace:</label> <select name="outputns" id="outputns">
%for (code,ns) in namespaces:
    <option name="{{code}}">{{ns}}</option>
%end
<p><label for="outputformat">Output Format:</label> <select name="outputformat" id="outputformat">
    <option value="html" selected="true">Human Readable (HTML)</option>
    <option value="csv">Tab Separated</option>
    <option value="json">JSON</option>
</select>

<h2>Offlline Use</h2>

<p>You can access the same functionality through a convenient Python interface.</P>

% rebase base title='Waldo Identifier Translation'
