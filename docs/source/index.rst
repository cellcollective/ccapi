CCPy
====

A Python Client Library for the `Cell Collective <https://cellcollective.org>`_ API

.. image:: https://img.shields.io/pypi/v/ccpy.svg?style=flat-square
    :target: https://pypi.org/project/ccpy/

.. image:: https://img.shields.io/pypi/l/ccpy.svg?style=flat-square
    :target: https://pypi.org/project/ccpy/

.. image:: https://img.shields.io/pypi/pyversions/ccpy.svg?style=flat-square
    :target: https://pypi.org/project/ccpy/

**CCPy** is a Python Package that provides a simple interface to 
`Cell Collective <https://cellcollective.org>`_ for modelling and analysis of 
biological networks.

-------------------

    >>> import cc
    >>> client = cc.Client()
    >>> model  = client.read("sample.sbml")
    >>> model.species[:3]
    [<Species id=-1026 name='MMP3'>,
     <Species id=-1028 name='MMP1'>,
     <Species id=-1030 name='MMP1'>]

**CCPy** includes simple, object-oriented interfaces for creating and 
reading models (to/from an SBML file format), graphically viewing such models, 
editing, saving and exporting models (into SBML, Boolean Expressions, 
Truth Tables, Interaction Matrix, etc. formats).

    >>> model.summary()
    Internal Components (+, -) External Components
    -------------------------- -------------------
    AKT_T (8,0)                PI3K
    CARMA1_T (1,0)             GP63_L
    IKK_BETA_T (0,3)           CRE_T

Beloved Features
----------------

**CCPy** attempts to be an all-in-one toolbox for modelling biological systems.

- Reading public and private models.
- Rich Knowledge-Base for each model species.
- Importing models using an SBML file format.
- Exporting models into SBML, Boolean Expressions, Truth Tables, etc.
- Querying for models.
- Visualizing models graphically.

**CCPy** officially supports Python 3.4+.

The User Guide
--------------

.. toctree::
   :maxdepth: 2

   user/quickstart
   user/modelling

The API Guide
-------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api