.. _installation:

Installation
============

This part of the documentation covers the installation of **ccapi**. 
The first step to using any software package is getting it properly installed.

Installation via ``pip``
------------------------

The recommended way to install **ccapi** is via ``pip``.

.. code-block:: console

   $ pip install ccapi

For instructions on installing python and pip see "The Hitchhiker's Guide to
Python" `Installation Guides
<http://docs.python-guide.org/en/latest/starting/installation/>`_.

Installation of optional dependencies
-------------------------------------

You can install all packages directly by:

.. code-block:: console

   $ pip install ccapi[all]

Building from source
--------------------

**ccapi** is actively developed on `GitHub <https://github.com/achillesrasquinha/ccapi>`_ 
and is always avaliable.

You can clone the base repository with :code:`git` as follows:

.. code-block:: console

    $ git clone git@github.com:achillesrasquinha/ccapi.git

Optionally, you could download the 
`tarball <https://github.com/achillesrasquinha/tarball/ccapi>`_ or 
`zipball <https://github.com/achillesrasquinha/zipball/ccapi>`_ as follows:

**For Linux Users**

.. code-block:: console

	$ curl -OL https://github.com/achillesrasquinha/tarball/ccapi

**For Windows Users**

.. code-block:: console

	$ curl -OL https://github.com/achillesrasquinha/zipball/ccapi

Install necessary dependencies

.. code-block:: console

    $ cd ccapi
    $ pip install -r requirements.txt

Then, go ahead and install **ccapi** in your site-packages  as follows:

.. code-block:: console

    $ python setup.py install

Check to see if you've installed **ccapi** correctly.

.. code-block:: python

	>>> import ccapi