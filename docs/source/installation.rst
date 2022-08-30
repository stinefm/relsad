.. highlight:: shell

============
Installation
============

--------------
Stable release
--------------

To install relsad, run this command in your terminal:

.. code-block:: console

    $ pip install --upgrade pip
    $ pip install relsad

This is the preferred method to install relsad, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


------------
From sources
------------

The sources for relsad can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/stinefm/relsad

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/stinefm/relsad/tarball/main

Once you have a copy of the source, you can install it. The method of installation will depend on the packaging library being used.

Install relsad with:

.. code-block:: console

    $ pip install --upgrade pip
    $ pip install poetry
    $ poetry install


.. _Github repo: https://github.com/stinefm/relsad
.. _tarball: https://github.com/stinefm/relsad/tarball/master


----------------
Test the package
----------------

If you installed relsad from source, you should run the tests to validate the installation. This is done by calling pytest from the repo:

.. code-block:: console

    $ poetry run pytest
