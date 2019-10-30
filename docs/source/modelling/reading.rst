.. _reading:

Reading a Model
===============

CCPy supports reading and writing models in the SBML, JSON, YAML, and pickle 
formats. The JSON and YAML formats may be more useful for CCPy-specific 
functionality.

The package also ships with test models in various formats for testing 
purposes.

    >>> from os.path import join
    >>> from cc.constant import DATA_DIRECTORY

SBML
----

The `Systems Biology Markup Language <http://sbml.org>`_ is an XML-based 
standard format for distributing models.

    >>> model = client.read(join(DATA_DIRECTORY, "fibroblasts.sbml"))