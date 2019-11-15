.. _loading:

Loading a Model
===============

This simple example demonstrates how to load a model from Cell Collective.

First, :ref:`create a Client object with CCPy <instantize_client>` by typing

    >>> import cc
    >>> client = cc.Client()

To load models from an account, type:

    >>> models = client.get("model")
    >>> models
    [<Model id=2309  name='EGFR & ErbB S...'>,
     <Model id=5128  name='Lac Operon'>,
     <Model id=10248 name='Bacteriophage...'>,
     <Model id=2314  name='IL-6 Signalli...'>,
     <Model id=16659 name='Modeling Ligh...'>]

By default, :func:`client.get` loads a maximum of ``cc.constant.MAXIMUM_API_RESOURCE_FETCH``
models for each request. To fetch more, simply paginate as follows:

    >>> models = client.get("model", since = 6)
    >>> models
    [<Model id=16659 name='Modeling Ligh...'>,
     <Model id=1557  name='Signal Transd...'>,
     <Model id=6678  name='CD4+ T cell D...'>,
     <Model id=2329  name='Apoptosis Net...'>,
     <Model id=17433 name='Simulating th...'>]
                                            
Consider a publically available model with ID 2309. We can fetch a model by
its ID as follows:

    >>> model = client.get("model", id_ = 2309)

Each model provides you a list of species objects:

    >>> len(model.species)
    104
    >>> model.species[:3]
    [<Species id=128127 name='elk1'>,
     <Species id=128129 name='stat1'>,
     <Species id=128128 name='shc'>]

When using `Jupyter Notebook <https://jupyter.org/>`_, this type of information 
is rendered as follows:

Components
----------

Regulators
----------

Conditions
----------

Sub Conditions
--------------