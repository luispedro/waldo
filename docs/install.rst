================
Installing Waldo
================


Getting the code
----------------

If you use ``pip`` or ``easy_install``, you should be able to install waldo
with::

    pip install waldo
    easy_install waldo

If you prefer to install from source, you can get either `the released version
<>`__ or the `bleeding edge <https://github.com/luispedro/waldo>`__.

Once you download the code, you should be able to install it with:: 

    python setup.py install

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


Downloading and building the database
-------------------------------------

::

    update-waldo --user --unsafe --verbose

The ``--user`` flag installs the database just for this user (but does not
require super-user [root] permissions).

The ``--unsafe`` flag makes the process much faster. However, it also means
that if the process is interrupted, it will need to be started from scratch.

The ``--verbose`` flag, as expected, make the whole process more verbose.
