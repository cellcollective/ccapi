.. _quickstart:

Getting Started
===============

Eager to get started? This page gives a good introduction in how to get started with ccpaw.

First, make sure that:

* ccpaw is installed
* ccpaw is up-to-date

Let’s get started with some simple examples.

.. _instantize_client:

Instantizing a Client object
----------------------------

Creating a Client object with ccpaw is very simple.

Begin by importing the ccpaw module:

    >>> import ccpaw

Now, let’s try to create a client object.

    >>> client = ccpaw.Client()

Now, we have a Client object called client. We can get all the information we need from this object.

Authenticating via Password Flow
--------------------------------

Before you can authenticate using ccpaw, you must first register an 
application of the appropriate type on 
`Cell Collective <https://cellcollective.org>`_ . If you do not require a 
user context, it is read only.

In order to use a password flow application with ccpaw you need the following 
pieces of information:

``email`` - The email address of the Cell Collective account used to 
register the application.
``password`` - The password for the Cell Collective account used to register 
the application.

With this information, authorizing is as simple as:

    >>> client.auth(email = "test@cellcollective.org", password = "test")

To verify that you are authenticated as the correct user, run:

    >>> client.me()
    <User 10887 at 0x01118bf850 name='Test Test'>

The output should contain the same name as your Cell Collective account.

You can also check if you're authenticated as follows:

    >>> client.authenticated
    True

If the following exception is raised, double check your credentials and ensure 
that that the email address and password you passed are valid.

.. code:: shell

    AuthenticationError: Unable to login into Cell Collective with credentials provided.

Authenticating via Authorization Token
--------------------------------------

You can also authenticate by passing an already available authorization token.

    >>> client.auth(token = "<YOUR_AUTHORIZATION_TOKEN>")
    >>> client.authenticated
    True

Logging in ccpaw
---------------

Occasionally it is useful to observe the HTTP requests that ccpaw is issuing.
To do so you have to configure and enable logging.

To log everything available, import the `logging` module:

    >>> import ccpaw, logging

Create a logger instance of a logger of name `cc` and set its level to `DEBUG`.

    >>> logger = logging.getLogger("cc")
    >>> logger.setLevel(logging.DEBUG)

When properly configured, HTTP requests that are issued should produce output 
similar to one below.

    >>> client = ccpaw.Client()
    2019-11-23 14:23:37,547 | INFO | Dispatching a GET request to URL: https://cellcollective.org/api/ping with Arguments - {}
    >>> client
    <Client url='https://cellcollective.org'>

For more information on logging, see `logging.Logger <https://docs.python.org/3/library/logging.html>`_.