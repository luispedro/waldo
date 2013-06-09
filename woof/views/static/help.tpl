<h1>User Guide</h1>
<h2>User interface</h2>
<p>The web interface to waldo is very simple. You look up a protein and it
returns whatever its databases know about it.</p>

<h2>Programmatic interface</h2>
<p>Waldo can also be installed locally and programmatically queried. This is
more appropriate for heavy usage.</p>

<h3>Example</h3>
<pre>
import waldo.uniprot.retrieve
from waldo.go import id_to_term

name = 'ACTB_HUMAN'
gos = waldo.uniprot.retrieve.retrieve_go_annotations('name')

for g in gos:
    print id_to_term(g)
</pre>
<p>This prints out:

<ul>
    <li>axon</li>
    <li>ortical cytoskeleton</li>
    <li>ytoskeleton</li>
    <li>ytosol</li>
    <li>xtracellular vesicular exosome</li>
    <li>LL5-L complex</li>
    <li>uA4 histone acetyltransferase complex</li>
    <li>ostsynaptic density</li>
    <li>ibonucleoprotein complex</li>
</ul>


<h3>Install</h3>
<p>Please download the Python package from <a
href="http://pypi.python.org/packages/waldo">PyPI</a> or <a
href="http://github.com/luispedro/waldo">github</a>.</p>
<p>You can probably install it with one of the following two commands</p>
<pre>
pip install waldo
easy_install waldo
</pre></p>

<p>After installation, run

<pre>
update-waldo --user --unsafe
</pre>

to install the database.</p>


<h3>Online Documentation</h3>

<p>Further online documentation is available at <a href="http://waldo.readthedocs.org/en/latest/">read the docs</a>.</p>

%rebase base title='Help'
