.. _modelling:

Modelling
=========

Reading a Model
---------------

This simple example demonstrates how to read a model from an SBML file.

First, :ref:`create a Client object with CCPy <instantize_client>` as follows.

    >>> import cc
    >>> client = cc.Client()

CCPy supports reading and writing models in the SBML, JSON, YAML, and pickle 
formats. The JSON and YAML formats may be more useful for CCPy-specific 
functionality.

The package also ships with test models in various formats for testing 
purposes.

    >>> from os.path   import join
    >>> from cc.config import PATH

SBML
----

The `Systems Biology Markup Language <http://sbml.org>` is an XML-based 
standard format for distributing models.

    >>> model = client.read(join(PATH["DATA"], "fibroblasts.sbml"))