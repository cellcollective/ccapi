.. _quickstart:

Quickstart
==========

Eager to get started? This page gives a good introduction in how to get started with CCPy.

First, make sure that:

* CCPy is installed
* CCPy is up-to-date

Let’s get started with some simple examples.

.. _instantize_client:

Instantizing a Client object
----------------------------

Creating a Client object with CCPy is very simple.

Begin by importing the CCPy module:

    >>> import cc

Now, let’s try to create a client object.

    >>> client = cc.Client()

Now, we have a Client object called client. We can get all the information we need from this object.

Authenticating via Password Flow
--------------------------------

Before you can authenticate using CCPy, you must first register an 
application of the appropriate type on 
`Cell Collective <https://cellcollective.org>`_ . If you do not require a 
user context, it is read only.

In order to use a password flow application with CCPy you need the following 
pieces of information:

``email`` - The email address of the Cell Collective account used to 
register the application.
``password`` - The password for the Cell Collective account used to register 
the application.

With this information, authorizing is as simple as:

    >>> client.auth(email = "test@cellcollective.org", password = "test")

To verify that you are authenticated as the correct user, run:

    >>> client.me()
    <User id=10887 name='Test Test'>

The output should contain the same name as your Cell Collective account.

You can also check if you're authenticated as follows:

    >>> client.authenticated
    True

If the following exception is raised, double check your credentials and ensure 
that that the email address and password you passed are valid.

.. code:: shell

    AuthenticationError: Unable to login into Cell Collective with credentials provided.