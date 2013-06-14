<h2>Identifier Translation</h2>
% if results is not None:


    <h3>Results</h3>
    <p>Waldo uses Ensembl IDs as an intermediate step.</p>

    <p><a href="#" id="resultstoggle">Show just final output (for easy copy &amp; paste)</a></p>
    <script>
        var full = true;
        $('#resultstoggle').click(function() {
            if (full) {
                $('#fullresults').hide();
                $('#justoutput').show();
                $('#resultstoggle').text('Show full output');
            } else {
                $('#fullresults').show();
                $('#justoutput').hide();
                $('#resultstoggle').text('Show just final output');
            }
            full = !full;
        });
    </script>

    <style>
#fullresults TH {
    border-top: solid 3px black;
    border-bottom: solid 2px black;
    background: #ccc;
    padding-right: 4em;
}
#fullresults {
    border-bottom: solid 3px black;
}
    </style>
    <table id="fullresults">
    <tr>
    <th>Input ({{ inputns_user }})</th>
    <th>Ensembl</th>
    <th>Output ({{ outputns_user }})</th>
    </tr>
    %for r in results:
    <tr>
        <td>{{ r[0] }}</td>
        <td>{{ r[1] }}</td>
        <td>{{ r[2] }}</td>
    </tr>
    %end
    </table>

    <div id="justoutput">
        <pre>
        %for r in results:
            {{ r[2] }}
        %end
        </pre>
    </div>
    <script>$('#justoutput').hide();</script>

% end
<h3>New Query</h3>
<form action="/translate" method="post">
<p><label for="inputns">Input Namespace:</label> <select name="inputns" id="inputns">
%for (code,ns) in namespaces:
    <option value="{{code}}">{{ns}}</option>
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
    <option value="{{code}}">{{ns}}</option>
%end
<p><label for="outputformat">Output Format:</label> <select name="outputformat" id="outputformat">
    <option value="html" selected="true">Human Readable (HTML)</option>
    <option value="csv">Tab Separated</option>
    <option value="json">JSON</option>
</select>
<input type="Submit" />
</form>

<h2>Offlline Use</h2>

<p>You can access the same functionality through a convenient Python interface.</P>

<ol>
    <li><a href="https://pypi.python.org/pypi/waldo">Download</a> and <a href="http://waldo.readthedocs.org/en/latest/install.html">install</a> waldo</li>
    <li><a href="http://waldo.readthedocs.org/en/latest/identifiers.html">Learn how to map identifiers in Python</a></li>
</ol>

% rebase base title='Waldo Identifier Translation'
