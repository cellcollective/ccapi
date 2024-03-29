ccapi
===

Release v\ |version|. (:ref:`Installation <install:>`)

.. image:: https://img.shields.io/travis/achillesrasquinha/ccapi.svg?style=flat-square
    :target: https://travis-ci.org/achillesrasquinha/ccapi
    
.. image:: https://img.shields.io/appveyor/ci/achillesrasquinha/ccapi.svg?style=flat-square&logo=appveyor
    :target: https://ci.appveyor.com/project/achillesrasquinha/ccapi

.. image:: https://img.shields.io/coveralls/github/achillesrasquinha/ccapi.svg?style=flat-square
    :target: https://coveralls.io/github/achillesrasquinha/ccapi

.. image:: https://img.shields.io/pypi/pyversions/ccapi.svg?style=flat-square
    :target: https://pypi.org/project/ccapi/

.. image:: https://img.shields.io/docker/build/achillesrasquinha/ccapi.svg?style=flat-square&logo=docker
    :target: https://hub.docker.com/r/achillesrasquinha/ccapi

.. image:: https://img.shields.io/badge/made%20with-boilpy-red.svg?style=flat-square
    :target: https://git.io/boilpy

.. image:: https://img.shields.io/badge/Say%20Thanks-🦉-1EAEDB.svg?style=flat-square
    :target: https://saythanks.io/to/achillesrasquinha

.. image:: https://img.shields.io/badge/donate-💵-f44336.svg?style=flat-square
    :target: https://paypal.me/achillesrasquinha

A Python Library to interact with the `Cell Collective <https://cellcollective.org>`_ API v2

**ccapi** is a Python Package that provides a simple interface to 
`Cell Collective <https://cellcollective.org>`_ for modelling and analysis of 
biological networks.

-------------------

    >>> import ccapi
    >>> model   = ccapi.load_model("fibroblasts") # a boolean-based model
    >>> boolean = model.version[0]
    >>> boolean.components
    [<ExternalComponent -2 at 0x0111ab9a50 name='ExtPump'>,
     <ExternalComponent -3 at 0x0111ab9a90 name='alpha_1213L'>,
     <ExternalComponent -4 at 0x0111ab9ad0 name='alpha_iL'>]

**ccapi** includes simple, object-oriented interfaces for creating and 
reading models (to/from an `SBML qual <http://www.colomoto.org/formats/sbml-qual.html>`_ file format), graphically viewing such models, 
querying, editing, saving and exporting models (into SBML qual, Boolean Expressions, 
Truth Tables, Interaction Matrix and GML formats).

    >>> boolean.summary()
    Internal Components (+, -) External Components
    -------------------------- -------------------
    Palpha_iR (1,0)            ExtPump            
    Cbp (1,0)                  alpha_1213L        
    EGFR (3,0)                 alpha_iL           
    PIP2_45 (3,0)              alpha_sL
    ...

Beloved Features
----------------

**ccapi** attempts to be an all-in-one toolbox for modelling biological systems.

- Reading public and private models from `Cell Collective <https://cellcollective.org>`_.
- A rich knowledge-base for each model species.
- Importing models using an SBML file format.
- Exporting models into SBML qual, Boolean Expressions, Truth Tables, Interaction Matrix and GML formats.
- Querying for models.
- Visualizing models graphically.

**ccapi** officially supports Python 2.7+ and 3.4+.

The User Guide
--------------

This part of the documentation, which is mostly prose, begins with some 
background information about **ccapi**, then focuses on step-by-step 
instructions for getting the most out of **ccapi**.

.. toctree::
   :maxdepth: 2

   user/installation
   user/quickstart

   notebooks/examples/global-configuration
   notebooks/examples/inspecting-model
   notebooks/examples/building-boolean-models
   notebooks/examples/reading-writing-boolean-models
   notebooks/examples/loading-models

Integrations
------------

.. toctree::

   notebooks/integrations/biomodels
   notebooks/integrations/ginsim

The API Guide
-------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api
