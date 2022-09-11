.. highlight:: shell

============
Installation
============

To avoid the pitfalls of using system package managers for installing/managing
`Python`, we recommend you to check out
`pyenv <https://github.com/pyenv/pyenv>`_ (Linux) or 
`pyenv-win <https://github.com/pyenv-win/pyenv-win>`_ (Windows).

For now, `RELSAD` supports the following `Python` versions:

- 3.8
- 3.9
- 3.10

--------------
Stable release
--------------

To install `RELSAD`, run this command in your terminal:

.. code-block:: console

    $ python -m pip install --upgrade pip
    $ python -m pip install relsad

This is the preferred method to install `RELSAD`,
as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


------------
From sources
------------

The sources for `RELSAD` can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/stinefm/relsad

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/stinefm/relsad/tarball/main

Once you have a copy of the source, you can install it.
The method of installation will depend on the packaging library being used.

The packaging and dependency management of `RELSAD` is done through `poetry`.
Follow the `poetry installation guide <https://python-poetry.org/docs/#installation>`_
for installation details.

Install `RELSAD` in developer mode using `poetry`:

.. code-block:: console

    $ cd relsad
    $ poetry install


.. _Github repo: https://github.com/stinefm/relsad
.. _tarball: https://github.com/stinefm/relsad/tarball/master


----------------
Test the package
----------------

If you installed `RELSAD` from source, you should run the tests to validate the installation. This is done by calling pytest from the repo:

.. code-block:: console

    $ cd relsad
    $ poetry run pytest
