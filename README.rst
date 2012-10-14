Waldo: Where Proteins Are
-------------------------

Waldo tells what everyone already knows.

Installation
............

Dependencies

- python
- lxml
- sqlalchemy

Under a debian or Ubuntu system, the following commands will install all needed
packages::

    sudo apt-get install python-lxml
    sudo apt-get install python-sqlalchemy

You can run the ``install.sh`` file to get everything working. The individual
steps are::

    python setup.py install

This is the standard Python installation command. In order to start using
waldo, you need to download all the database files and build the index. The
utility script ``waldo-update`` should accomplish this::

    waldo-update --datadir /path/to/datadir

The ``datadir`` is where waldo will store the downloaded information. It
defaults to ``/var/lib/waldo/data``.

Links
.....

- github: https://github.com/luispedro/waldo
