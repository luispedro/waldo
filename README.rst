Waldo: Where Proteins Are
-------------------------

Waldo tells what everyone already knows.

We have a manuscript in preparation. If you use this in a publication, please
let us know so we can (to the best of our knowledge), give you the right
citation.

Installation
............

Dependencies
~~~~~~~~~~~~

- python
- lxml
- sqlalchemy
- bottle

bottle is only needed if wish to run the web application (i.e., if you only
using the local programming API, then you can skip this step).

Under a debian or Ubuntu system, the following commands will install all needed
packages::

    sudo apt-get install python-lxml
    sudo apt-get install python-sqlalchemy
    sudo apt-get install python-bottle

Installation
~~~~~~~~~~~~

You can run the ``install.sh`` file to get everything working::

    ./install.sh

The individual steps are::

    python setup.py install

This is the standard Python installation command. In order to start using
waldo, you need to download all the database files and build the index. The
utility script ``update-waldo`` should accomplish this::

    update-waldo --user
    update-waldo
    update-waldo --datadir /path/to/datadir --database database.sqlite3

There are three variations (shown above):

1. ``--user`` (the default for ``install.sh``) installs waldo locally for this
   user (under ``$HOME/.local/share/waldo``)
2. Without an argument, it installs it system-wide (you need to have write
   access to ``/var/lib/waldo``
3. You can specify exactly where to store the data.

The ``datadir`` is where waldo will store the downloaded information. It
defaults to ``/var/lib/waldo/data``. You can also specify where to store the
database file (default is ``/var/lib/waldo/waldo.sqlite3``).

Additionally, you can use the ``--unsafe`` flag to speed up the indexing, but
if you interrupt the process, the database may be broken::

    update-waldo --user --unsafe

Running the Webapp
..................

If you have installed waldo as above, you should execute::

    python woof/woof.py

Then point your browser to http://localhost:8000/

Links
.....

- documentation: http://waldo.readthedocs.org/en/latest/
- github: https://github.com/luispedro/waldo
