import pytest

import ccapi
from ccapi.util.environ import getenv

@pytest.fixture
def client():
    client = ccapi.Client()
    return client

@pytest.fixture
def auth_client(client):
    email       = getenv("TEST_EMAIL",    "test@cellcollective.org")
    password    = getenv("TEST_PASSWORD", "test")
    
    client.auth(email = email, password = password)

    return client